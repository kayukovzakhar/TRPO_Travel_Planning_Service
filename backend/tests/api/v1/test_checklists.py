from fastapi.testclient import TestClient
from app.core.config import settings
# Use fixture instead of helpers
# from tests.utils import create_test_user, get_auth_headers 
from typing import Dict
import random
from app import crud
from app.tests.utils import create_random_route
from sqlalchemy.orm import Session

# Remove test user constants
# TEST_USER_EMAIL = ...
# TEST_USER_PASSWORD = ...

def test_checklist_items_flow(client: TestClient, auth_headers: Dict[str, str]): # Add fixture
    # 1. Create user and route
    headers = auth_headers
    create_route_resp = client.post(f"{settings.API_V1_STR}/routes/", headers=headers, json={"name": "Route with Checklist"})
    assert create_route_resp.status_code == 200, create_route_resp.text
    route_data = create_route_resp.json()
    route_id = route_data["id"]
    checklist_id = route_data["checklist"]["id"]
    assert checklist_id is not None
    # Assert that initial items are populated
    initial_items = route_data["checklist"]["items"]
    assert len(initial_items) == len(SUGGESTED_PLACES_KALININGRAD)

    # 2. Get checklist items (should NOT be empty initially)
    get_items_resp = client.get(f"{settings.API_V1_STR}/routes/{route_id}/checklist/items/", headers=headers)
    assert get_items_resp.status_code == 200, get_items_resp.text
    items_list_get = get_items_resp.json()
    assert len(items_list_get) == len(SUGGESTED_PLACES_KALININGRAD)
    # Check one item description for sanity
    assert any(item["description"] == f"Посетить: {SUGGESTED_PLACES_KALININGRAD[0]['name']}" for item in items_list_get)

    # 3. Add a NEW item to the checklist
    item_desc = "Buy Souvenirs"
    add_item_resp = client.post(
        f"{settings.API_V1_STR}/routes/{route_id}/checklist/items/",
        headers=headers,
        json={"description": item_desc}
    )
    assert add_item_resp.status_code == 200, add_item_resp.text
    item_data = add_item_resp.json()
    assert item_data["description"] == item_desc
    new_item_id = item_data["id"]

    # 4. Get checklist items again (should contain initial + new item)
    get_items_resp_after_add = client.get(f"{settings.API_V1_STR}/routes/{route_id}/checklist/items/", headers=headers)
    items_list_after_add = get_items_resp_after_add.json()
    assert len(items_list_after_add) == len(SUGGESTED_PLACES_KALININGRAD) + 1
    assert any(item["id"] == new_item_id and item["description"] == item_desc for item in items_list_after_add)

    # 5. Update the NEW item
    update_item_resp = client.put(
        f"{settings.API_V1_STR}/routes/{route_id}/checklist/items/{new_item_id}",
        headers=headers,
        json={"completed": True}
    )
    assert update_item_resp.status_code == 200, update_item_resp.text
    updated_item_data = update_item_resp.json()
    assert updated_item_data["id"] == new_item_id
    assert updated_item_data["completed"] is True
    assert updated_item_data["description"] == item_desc # Description shouldn't change

    # 6. Delete the NEW item
    delete_item_resp = client.delete(f"{settings.API_V1_STR}/routes/{route_id}/checklist/items/{new_item_id}", headers=headers)
    assert delete_item_resp.status_code == 200, delete_item_resp.text

    # 7. Get checklist items again (should contain only initial suggested items)
    get_items_resp_after_delete = client.get(f"{settings.API_V1_STR}/routes/{route_id}/checklist/items/", headers=headers)
    items_list_after_delete = get_items_resp_after_delete.json()
    assert len(items_list_after_delete) == len(SUGGESTED_PLACES_KALININGRAD)
    assert not any(item["id"] == new_item_id for item in items_list_after_delete)

def test_checklist_items_forbidden(client: TestClient, auth_headers: Dict[str, str]): # Add fixture
    # Create route with user 1 (using the fixture)
    headers1 = auth_headers
    create_route_resp = client.post(f"{settings.API_V1_STR}/routes/", headers=headers1, json={"name": "Owner Route"})
    route_id = create_route_resp.json()["id"]
    
    # Get an item_id from the automatically added items
    get_items_resp = client.get(f"{settings.API_V1_STR}/routes/{route_id}/checklist/items/", headers=headers1)
    items = get_items_resp.json()
    assert len(items) > 0 # Should have suggested items
    item_id_to_test = items[0]["id"]

    # Create user 2 and get headers
    from tests.utils import create_test_user, get_auth_headers # Keep helpers for second user
    email2 = f"checklist_other_{random.randint(1000,9999)}@example.com"
    create_test_user(client, {"name": "Other", "email": email2, "password": "otherpass"})
    headers2 = get_auth_headers(client, email2, "otherpass")

    # Try to access/modify items of user 1's route with user 2
    get_resp = client.get(f"{settings.API_V1_STR}/routes/{route_id}/checklist/items/", headers=headers2)
    assert get_resp.status_code == 403

    post_resp = client.post(f"{settings.API_V1_STR}/routes/{route_id}/checklist/items/", headers=headers2, json={"description": "Other Item"})
    assert post_resp.status_code == 403

    put_resp = client.put(f"{settings.API_V1_STR}/routes/{route_id}/checklist/items/{item_id_to_test}", headers=headers2, json={"completed": True})
    assert put_resp.status_code == 403

    delete_resp = client.delete(f"{settings.API_V1_STR}/routes/{route_id}/checklist/items/{item_id_to_test}", headers=headers2)
    assert delete_resp.status_code == 403 

def test_read_checklist_for_route(client: TestClient, db: Session, auth_headers: Dict[str, str]):
    """Test retrieving the checklist associated with a specific route."""
    # 1. Create a route (this should auto-create the checklist)
    route = create_random_route(db, headers=auth_headers)
    
    # 2. Fetch the checklist via the route's endpoint
    response = client.get(
        f"{settings.API_V1_STR}/routes/{route.id}/checklist", 
        headers=auth_headers
    )
    assert response.status_code == 200, response.text
    checklist_data = response.json()
    
    # 3. Verify the checklist structure and items
    assert "id" in checklist_data
    assert checklist_data["route_id"] == route.id
    assert "items" in checklist_data
    
    # Check that items were populated (number fetched from DB, <= limit)
    checklist_items = checklist_data["items"]
    assert len(checklist_items) > 0
    assert len(checklist_items) <= 10 # Based on limit in crud_route
    assert all(item['description'].startswith("Посетить:") for item in checklist_items)
    
    # 4. Fetch the checklist directly via the checklist endpoint (using the ID)
    checklist_id = checklist_data["id"]
    direct_response = client.get(
        f"{settings.API_V1_STR}/checklists/{checklist_id}", 
        headers=auth_headers
    )
    assert direct_response.status_code == 200, direct_response.text
    direct_checklist_data = direct_response.json()
    assert direct_checklist_data["id"] == checklist_id
    # Ensure items are the same
    assert len(direct_checklist_data["items"]) == len(checklist_items) 