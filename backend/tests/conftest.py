import sys
import os
import pytest
import random # Import random

# Add project root to sys.path BEFORE importing any app modules
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from typing import Generator, Any, Dict # Import Dict
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool # Import StaticPool

# Define Test DB URL here
# Use a file-based SQLite DB in the tests directory for persistence
TEST_DB_URL = "sqlite:///./test.db" 
# Or use in-memory SQLite (requires StaticPool in engine creation)
# TEST_DB_URL = "sqlite:///:memory:"

# Create engine and session *before* importing app modules that might use them
engine = create_engine(
    TEST_DB_URL, 
    connect_args={"check_same_thread": False},
    # Use StaticPool if using in-memory, otherwise default pool is fine for file db
    # poolclass=StaticPool 
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Now import app modules
# Set environment variable *before* importing config/settings if relying on it there
os.environ['DATABASE_URL'] = TEST_DB_URL
from app.main import app
from app.db.session import get_db # Import original get_db
from app.db.base import Base
from app.core.config import settings # Import settings AFTER env var is set
from tests.utils import create_test_user, get_auth_headers # Import test utils

# Create tables once per session
@pytest.fixture(scope="session", autouse=True)
def create_test_tables():
    """Create database tables once before the test session starts."""
    # Clean up old DB file if it exists
    if TEST_DB_URL.startswith("sqlite:///") and TEST_DB_URL != "sqlite:///:memory:":
        db_file = TEST_DB_URL.split("///")[1]
        if os.path.exists(db_file):
            try:
                os.remove(db_file)
            except PermissionError:
                print(f"Warning: Could not remove old test DB file {db_file}")
    print(f"Creating tables for test database: {settings.DATABASE_URL}")
    Base.metadata.create_all(bind=engine)
    yield
    # Teardown is handled by pytest_sessionfinish

# Clean tables before each test
@pytest.fixture(scope="function", autouse=True)
def clean_tables():
    """Delete all data from tables before each test runs."""
    connection = engine.connect()
    transaction = connection.begin()
    # Iterate over tables in reverse order of creation for FK constraints
    for table in reversed(Base.metadata.sorted_tables):
        connection.execute(table.delete())
    transaction.commit()
    connection.close()

def override_get_db() -> Generator[Session, None, None]:
    """Dependency override for getting DB session in tests."""
    db = TestingSessionLocal()
    try:
        yield db # Provide the session to the test
    finally:
        db.close() # Ensure session is closed after test

# Apply the override to the app
app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="module")
def client() -> Generator[TestClient, None, None]:
    """Pytest fixture to create a TestClient instance per module."""
    with TestClient(app) as c:
        yield c

@pytest.fixture(scope="function") # Run for each test function
def auth_headers(client: TestClient) -> Dict[str, str]:
    """Pytest fixture to create a unique user and return auth headers."""
    # Generate unique email for each test function run to ensure isolation
    email = f"testuser_{random.randint(10000, 99999)}@example.com"
    password = "testpassword"
    user_data = {"name": "Test Fixture User", "email": email, "password": password}
    
    # Register user 
    create_test_user(client, user_data)
    
    # Get headers
    headers = get_auth_headers(client, email, password)
    return headers

# Teardown session: dispose engine and remove DB file
def pytest_sessionfinish(session, exitstatus):
    print("\nDisposing test engine...")
    engine.dispose()
    print("Removing test database file...")
    if TEST_DB_URL.startswith("sqlite:///") and TEST_DB_URL != "sqlite:///:memory:":
        db_file = TEST_DB_URL.split("///")[1]
        if os.path.exists(db_file):
            try:
                os.remove(db_file)
                print(f"Removed test DB file: {db_file}")
            except Exception as e:
                print(f"Error removing test DB file {db_file}: {e}")
        else:
            print("Test DB file not found, skipping removal.")

# Add more fixtures if needed, e.g., for creating test users, tokens, etc. 