from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool # Needed for SQLite in-memory testing

# Import the settings object
from app.core.config import settings

# Determine connect_args based on database type
connect_args = {}
if settings.DATABASE_URL and settings.DATABASE_URL.startswith("sqlite"):
    # Specific arguments for SQLite to allow usage across threads in tests
    connect_args = {"check_same_thread": False}
    # Use StaticPool for SQLite in-memory to ensure the same connection is used
    # This is crucial because the in-memory database exists only for the duration of the connection
    engine = create_engine(
        settings.DATABASE_URL,
        connect_args=connect_args,
        poolclass=StaticPool
    )
else:
    # Standard engine creation for PostgreSQL or other DBs
    engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)


# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 