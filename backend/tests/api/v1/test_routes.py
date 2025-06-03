from fastapi.testclient import TestClient
from app.core.config import settings
from typing import Dict
import random

# --- Route Tests --- 
def test_create_route_unauthorized(client: TestClient):
    response = client.post(f"{settings.API_V1_STR}/routes/", json={"name": "My First Route"})
    assert response.status_code == 401 # Expect unauthorized

def test_create_and_read_route(client: TestClient, auth_headers: Dict[str, str]):
    # Headers are now provided by the fixture
    headers = auth_headers
    
    # Create route
    route_name = "Kaliningrad Trip"
    create_response = client.post(
        f"{settings.API_V1_STR}/routes/", 
        headers=headers, 
        json={"name": route_name, "points": [{"name": "Museum of Ocean"}, {"name": "Cathedral"}]}
    )
    assert create_response.status_code == 200, create_response.text
    created_data = create_response.json()
    assert created_data["name"] == route_name
    assert "id" in created_data
    assert "owner_id" in created_data
    assert len(created_data["points"]) == 2
    assert created_data["points"][0]["name"] == "Museum of Ocean"
    assert created_data["points"][1]["name"] == "Cathedral"
    assert "checklist" in created_data # Checklist should be created automatically
    assert created_data["checklist"] is not None
    
    # --- Assert Checklist Items --- 
    assert "checklist" in created_data 
    assert created_data["checklist"] is not None
    checklist_items = created_data["checklist"]["items"]
    # Check that *some* items were added (we fetch 10 by default now)
    assert len(checklist_items) > 0 
    assert len(checklist_items) <= 10 # Based on limit in crud_route
    # Check if descriptions seem plausible (contain 'Посетить:')
    assert all(item['description'].startswith("Посетить:") for item in checklist_items)
    # --- End Assert Checklist Items --- 

    route_id = created_data["id"]

    # Read the created route by ID
    read_response = client.get(f"{settings.API_V1_STR}/routes/{route_id}", headers=headers)
    assert read_response.status_code == 200, read_response.text
    read_data = read_response.json()
    assert read_data["id"] == route_id
    assert read_data["name"] == route_name
    assert len(read_data["points"]) == 2

    # Read all routes for the user
    read_all_response = client.get(f"{settings.API_V1_STR}/routes/", headers=headers)
    assert read_all_response.status_code == 200, read_all_response.text
    all_routes_data = read_all_response.json()
    assert isinstance(all_routes_data, list)
    assert len(all_routes_data) >= 1
    assert any(r["id"] == route_id for r in all_routes_data)

def test_read_route_not_found(client: TestClient, auth_headers: Dict[str, str]):
    headers = auth_headers
    response = client.get(f"{settings.API_V1_STR}/routes/99999", headers=headers) # Non-existent ID
    assert response.status_code == 404

def test_read_route_forbidden(client: TestClient, auth_headers: Dict[str, str]):
    # Create route with user 1 (using the fixture)
    headers1 = auth_headers 
    create_response = client.post(f"{settings.API_V1_STR}/routes/", headers=headers1, json={"name": "User1 Route"})
    route_id = create_response.json()["id"]
    
    # Create user 2 and get their headers (using helpers directly here is fine)
    # Or create another fixture if preferred
    from tests.utils import create_test_user, get_auth_headers
    email2 = f"other_user_{random.randint(1000, 9999)}@example.com"
    create_test_user(client, {"name": "Other User", "email": email2, "password": "otherpass"})
    headers2 = get_auth_headers(client, email2, "otherpass")
    
    response = client.get(f"{settings.API_V1_STR}/routes/{route_id}", headers=headers2)
    assert response.status_code == 403 # Expect forbidden

def test_update_route(client: TestClient, auth_headers: Dict[str, str]):
    headers = auth_headers
    # Create a route first
    create_response = client.post(f"{settings.API_V1_STR}/routes/", headers=headers, json={"name": "Route to Update"})
    route_id = create_response.json()["id"]

    # Update the route
    new_name = "Updated Route Name"
    update_response = client.put(f"{settings.API_V1_STR}/routes/{route_id}", headers=headers, json={"name": new_name})
    assert update_response.status_code == 200, update_response.text
    updated_data = update_response.json()
    assert updated_data["id"] == route_id
    assert updated_data["name"] == new_name

def test_delete_route(client: TestClient, auth_headers: Dict[str, str]):
    headers = auth_headers
    # Create a route first
    create_response = client.post(f"{settings.API_V1_STR}/routes/", headers=headers, json={"name": "Route to Delete"})
    route_id = create_response.json()["id"]

    # Delete the route
    delete_response = client.delete(f"{settings.API_V1_STR}/routes/{route_id}", headers=headers)
    assert delete_response.status_code == 200, delete_response.text
    deleted_data = delete_response.json()
    assert deleted_data["id"] == route_id

    # Verify route is deleted
    read_response = client.get(f"{settings.API_V1_STR}/routes/{route_id}", headers=headers)
    assert read_response.status_code == 404

# --- Point Tests (within routes) ---
def test_add_update_delete_point(client: TestClient, auth_headers: Dict[str, str]):
    headers = auth_headers
    # Create a route
    create_route_resp = client.post(f"{settings.API_V1_STR}/routes/", headers=headers, json={"name": "Route for Points"})
    route_id = create_route_resp.json()["id"]

    # 1. Add a point
    point_name = "Kant Island"
    add_point_resp = client.post(
        f"{settings.API_V1_STR}/routes/{route_id}/points/", 
        headers=headers, 
        json={"name": point_name, "location": "Central Kaliningrad"}
    )
    assert add_point_resp.status_code == 200, add_point_resp.text
    point_data = add_point_resp.json()
    assert point_data["name"] == point_name
    assert point_data["location"] == "Central Kaliningrad"
    assert point_data["visited"] is False
    assert "id" in point_data
    point_id = point_data["id"]

    # Verify point is in the route
    read_route_resp = client.get(f"{settings.API_V1_STR}/routes/{route_id}", headers=headers)
    route_data = read_route_resp.json()
    assert any(p["id"] == point_id for p in route_data["points"])

    # 2. Update the point (mark as visited)
    update_point_resp = client.put(
        f"{settings.API_V1_STR}/routes/{route_id}/points/{point_id}",
        headers=headers,
        json={"visited": True, "name": "Kant Island (Visited)"}
    )
    assert update_point_resp.status_code == 200, update_point_resp.text
    updated_point_data = update_point_resp.json()
    assert updated_point_data["id"] == point_id
    assert updated_point_data["visited"] is True
    assert updated_point_data["name"] == "Kant Island (Visited)"

    # 3. Delete the point
    delete_point_resp = client.delete(f"{settings.API_V1_STR}/routes/{route_id}/points/{point_id}", headers=headers)
    assert delete_point_resp.status_code == 200, delete_point_resp.text
    assert delete_point_resp.json()["id"] == point_id

    # Verify point is removed from the route
    read_route_resp_after_delete = client.get(f"{settings.API_V1_STR}/routes/{route_id}", headers=headers)
    route_data_after_delete = read_route_resp_after_delete.json()
    assert not any(p["id"] == point_id for p in route_data_after_delete["points"]) 