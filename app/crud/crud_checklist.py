from sqlalchemy.orm import Session
from typing import Optional

from app.models.checklist import Checklist
from app.models.route import Route # Import Route to potentially create checklist
from app.api.v1.schemas.checklist import ChecklistCreate, ChecklistUpdate

def get_checklist(db: Session, checklist_id: int) -> Optional[Checklist]:
    """Gets a checklist by ID."""
    return db.query(Checklist).filter(Checklist.id == checklist_id).first()

def get_checklist_by_route(db: Session, route_id: int) -> Optional[Checklist]:
    """Gets the checklist associated with a specific route."""
    return db.query(Checklist).filter(Checklist.route_id == route_id).first()

# Checklist is typically created automatically when a Route is created.
# We might need a function to ensure a checklist exists or create one if needed.
def get_or_create_checklist_for_route(db: Session, route_id: int) -> Checklist:
    """Gets the checklist for a route, creating one if it doesn't exist."""
    db_checklist = get_checklist_by_route(db, route_id=route_id)
    if not db_checklist:
        db_checklist = Checklist(route_id=route_id)
        db.add(db_checklist)
        db.commit()
        db.refresh(db_checklist)
    return db_checklist

# Update might be added later if checklists get editable properties
# def update_checklist(db: Session, db_checklist: Checklist, checklist_in: ChecklistUpdate) -> Checklist:
#     ... 