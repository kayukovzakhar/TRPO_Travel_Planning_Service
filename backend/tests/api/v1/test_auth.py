from fastapi.testclient import TestClient
from app.core.config import settings # To get the API prefix

# Basic test for registration
def test_register_user(client: TestClient):
    response = client.post(
        f"{settings.API_V1_STR}/auth/register",
        json={"name": "Test User", "email": "test@example.com", "password": "testpassword"},
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["name"] == "Test User"
    assert "id" in data
    assert "hashed_password" not in data # Ensure password is not returned

# Test registration with existing email
def test_register_existing_user(client: TestClient):
    # First registration (should succeed)
    client.post(
        f"{settings.API_V1_STR}/auth/register",
        json={"name": "Test User 2", "email": "test2@example.com", "password": "testpassword2"},
    )
    # Second registration with the same email (should fail)
    response = client.post(
        f"{settings.API_V1_STR}/auth/register",
        json={"name": "Test User 3", "email": "test2@example.com", "password": "testpassword3"},
    )
    assert response.status_code == 400, response.text
    assert response.json() == {"detail": "Email already registered"}

# Test successful login
def test_login_user(client: TestClient):
    # Register user first
    client.post(
        f"{settings.API_V1_STR}/auth/register",
        json={"name": "Login Test", "email": "login@example.com", "password": "loginpass"},
    )
    # Attempt login
    login_data = {"username": "login@example.com", "password": "loginpass"}
    response = client.post(
        f"{settings.API_V1_STR}/auth/login", data=login_data
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

# Test login with incorrect password
def test_login_incorrect_password(client: TestClient):
    client.post(
        f"{settings.API_V1_STR}/auth/register",
        json={"name": "Login Fail", "email": "loginfail@example.com", "password": "correctpass"},
    )
    login_data = {"username": "loginfail@example.com", "password": "wrongpass"}
    response = client.post(
        f"{settings.API_V1_STR}/auth/login", data=login_data
    )
    assert response.status_code == 401, response.text
    assert response.json() == {"detail": "Incorrect email or password"}

# Test login with non-existent user
def test_login_nonexistent_user(client: TestClient):
    login_data = {"username": "nosuchuser@example.com", "password": "somepass"}
    response = client.post(
        f"{settings.API_V1_STR}/auth/login", data=login_data
    )
    assert response.status_code == 401, response.text
    assert response.json() == {"detail": "Incorrect email or password"}

# Test accessing protected route /users/me
def test_read_users_me(client: TestClient):
    # Register and login to get token
    reg_response = client.post(
        f"{settings.API_V1_STR}/auth/register",
        json={"name": "Me Test", "email": "me@example.com", "password": "mypassword"},
    )
    assert reg_response.status_code == 200, reg_response.text
    
    login_response = client.post(
        f"{settings.API_V1_STR}/auth/login", 
        data={"username": "me@example.com", "password": "mypassword"}
    )
    assert login_response.status_code == 200, login_response.text
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Access protected route
    response = client.get(f"{settings.API_V1_STR}/auth/users/me", headers=headers)
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["email"] == "me@example.com"
    assert data["name"] == "Me Test"
    assert "id" in data

# Test accessing protected route without token
def test_read_users_me_no_token(client: TestClient):
    response = client.get(f"{settings.API_V1_STR}/auth/users/me")
    assert response.status_code == 401, response.text
    # FastAPI 0.100+ uses this detail for OAuth2PasswordBearer without token
    assert response.json() == {"detail": "Not authenticated"}

# Test accessing protected route with invalid token
def test_read_users_me_invalid_token(client: TestClient):
    headers = {"Authorization": "Bearer invalidtoken"}
    response = client.get(f"{settings.API_V1_STR}/auth/users/me", headers=headers)
    assert response.status_code == 401, response.text
    # Detail might vary slightly based on JWTError, but should indicate invalid credentials
    assert response.json()["detail"] == "Could not validate credentials" 