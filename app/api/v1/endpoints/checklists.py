from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Any

from app import crud, models # Import top-level crud, models
from app.api.v1 import schemas # Import schemas from correct path
from app.api import deps
from app.db.session import get_db

# Router will be included with prefix /routes/{route_id}/checklist
router = APIRouter()

# Helper function to get checklist and check ownership
async def get_checklist_and_verify_owner(
    route_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(deps.get_current_active_user)
) -> models.Checklist:
    route = crud.get_route(db, route_id=route_id)
    if not route:
        raise HTTPException(status_code=404, detail="Route not found")
    if route.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    # Ensure checklist exists for the route
    checklist = crud.get_or_create_checklist_for_route(db=db, route_id=route_id)
    return checklist

@router.get("/items/", response_model=List[schemas.Item])
def read_checklist_items(
    route_id: int, # Comes from the path prefix
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    checklist: models.Checklist = Depends(get_checklist_and_verify_owner) # Verify owner and get checklist
) -> Any:
    """Retrieve items for the checklist of a specific route."""
    items = crud.get_items_by_checklist(db, checklist_id=checklist.id, skip=skip, limit=limit)
    return items

@router.post("/items/", response_model=schemas.Item)
def create_checklist_item(
    route_id: int,
    *,
    item_in: schemas.ItemCreate,
    db: Session = Depends(get_db),
    checklist: models.Checklist = Depends(get_checklist_and_verify_owner)
) -> Any:
    """Create a new item in the checklist for a specific route."""
    item = crud.create_checklist_item(db=db, item=item_in, checklist_id=checklist.id)
    return item

@router.put("/items/{item_id}", response_model=schemas.Item)
def update_checklist_item(
    route_id: int,
    item_id: int,
    *,
    item_in: schemas.ItemUpdate,
    db: Session = Depends(get_db),
    checklist: models.Checklist = Depends(get_checklist_and_verify_owner)
) -> Any:
    """Update an item in the checklist."""
    item = crud.get_item(db=db, item_id=item_id)
    if not item or item.checklist_id != checklist.id:
        raise HTTPException(status_code=404, detail="Item not found in this checklist")
    item = crud.update_item(db=db, db_item=item, item_in=item_in)
    return item

@router.delete("/items/{item_id}", response_model=schemas.Item)
def delete_checklist_item(
    route_id: int,
    item_id: int,
    *,
    db: Session = Depends(get_db),
    checklist: models.Checklist = Depends(get_checklist_and_verify_owner)
) -> Any:
    """Delete an item from the checklist."""
    item = crud.get_item(db=db, item_id=item_id)
    if not item or item.checklist_id != checklist.id:
        raise HTTPException(status_code=404, detail="Item not found in this checklist")
    deleted_item = crud.delete_item(db=db, item_id=item_id)
    return deleted_item 