from fastapi.testclient import TestClient
from typing import Dict, Any

from app.core.config import settings


def create_test_user(client: TestClient, user_data: Dict[str, str]) -> Dict[str, Any]:
    """Helper function to register a user for testing."""
    response = client.post(f"{settings.API_V1_STR}/auth/register", json=user_data)
    assert response.status_code == 200, f"Failed to register user {user_data.get('email')}: {response.text}"
    return response.json()

def get_auth_headers(client: TestClient, email: str, password: str) -> Dict[str, str]:
    """Helper function to log in a user and get Authorization headers."""
    login_data = {"username": email, "password": password}
    response = client.post(f"{settings.API_V1_STR}/auth/login", data=login_data)
    assert response.status_code == 200, f"Failed to login user {email}: {response.text}"
    token_data = response.json()
    access_token = token_data["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    return headers 