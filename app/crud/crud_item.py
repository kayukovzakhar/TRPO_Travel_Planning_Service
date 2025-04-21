from sqlalchemy.orm import Session
from typing import List, Optional

from app.models.item import Item
from app.api.v1.schemas.item import ItemCreate, ItemUpdate

def get_item(db: Session, item_id: int) -> Optional[Item]:
    """Gets an item by ID."""
    return db.query(Item).filter(Item.id == item_id).first()

def get_items_by_checklist(db: Session, checklist_id: int, skip: int = 0, limit: int = 100) -> List[Item]:
    """Gets all items for a specific checklist."""
    return db.query(Item).filter(Item.checklist_id == checklist_id).offset(skip).limit(limit).all()

def create_checklist_item(db: Session, item: ItemCreate, checklist_id: int) -> Item:
    """Creates a new item associated with a checklist."""
    db_item = Item(**item.model_dump(), checklist_id=checklist_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def update_item(db: Session, db_item: Item, item_in: ItemUpdate) -> Item:
    """Updates an existing item."""
    item_data = item_in.model_dump(exclude_unset=True)
    for key, value in item_data.items():
        setattr(db_item, key, value)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def delete_item(db: Session, item_id: int) -> Optional[Item]:
    """Deletes an item by ID."""
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if db_item:
        db.delete(db_item)
        db.commit()
    return db_item 