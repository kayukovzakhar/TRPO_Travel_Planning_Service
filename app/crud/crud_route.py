from sqlalchemy.orm import Session
from typing import List, Optional

from app.models.route import Route
from app.models.point import Point
from app.api.v1.schemas.route import RouteCreate, RouteUpdate
from app.api.v1.schemas.point import PointCreate # Needed for creating points with route
from app.api.v1.schemas.item import ItemCreate # Import ItemCreate schema
from .crud_checklist import get_or_create_checklist_for_route # Import checklist creator
from .crud_item import create_checklist_item # Import item creator
from .crud_place import get_places # Import get_places
from app.crud.base import CRUDBase

def get_route(db: Session, route_id: int) -> Optional[Route]:
    """Gets a route by ID, eagerly loading points."""
    # Using options(selectinload(Route.points)) is implicitly handled by lazy='selectin' in the model
    return db.query(Route).filter(Route.id == route_id).first()

def get_routes_by_owner(db: Session, owner_id: int, skip: int = 0, limit: int = 100) -> List[Route]:
    """Gets all routes for a specific owner."""
    return (
        db.query(Route)
        .filter(Route.owner_id == owner_id)
        .offset(skip)
        .limit(limit)
        .all()
    )

def create_owner_route(db: Session, route: RouteCreate, owner_id: int) -> Route:
    """Creates a new route, its checklist, adds suggested items from DB, and associated points."""
    # Create Route object without points first
    db_route = Route(name=route.name, owner_id=owner_id)
    db.add(db_route)
    db.commit() 
    db.refresh(db_route)

    # Ensure checklist is created for this route
    db_checklist = get_or_create_checklist_for_route(db=db, route_id=db_route.id)

    # --- Auto-populate checklist with suggested places from DB --- 
    suggested_places = get_places(db=db, limit=10) # Get some suggested places (limit for now)
    for place in suggested_places:
        item_in = ItemCreate(description=f"Посетить: {place.name}") # Use place.name
        create_checklist_item(db=db, item=item_in, checklist_id=db_checklist.id)
    # --- End auto-populate --- 

    # Now create associated points if any were provided in the request
    if route.points:
        for point_data in route.points:
            db_point = Point(**point_data.model_dump(), route_id=db_route.id)
            db.add(db_point)
        # Commit points after adding them all
        db.commit()

    # Refresh the route again to load the created points AND checklist items
    db.refresh(db_route)
    # Explicitly refresh the checklist to load items if needed immediately in response
    # This might not be necessary depending on relationship loading strategy
    # db.refresh(db_checklist)
    return db_route

def update_route(db: Session, db_route: Route, route_in: RouteUpdate) -> Route:
    """Updates an existing route (currently only name)."""
    route_data = route_in.model_dump(exclude_unset=True)
    for key, value in route_data.items():
        setattr(db_route, key, value)
    db.add(db_route)
    db.commit()
    db.refresh(db_route)
    return db_route

def delete_route(db: Session, route_id: int) -> Optional[Route]:
    """Deletes a route by ID. Cascading delete handles associated points."""
    db_route = db.query(Route).filter(Route.id == route_id).first()
    if db_route:
        db.delete(db_route)
        db.commit()
    return db_route 

class CRUDRoute(CRUDBase[Route, RouteCreate, RouteUpdate]):
    def get_multi_by_owner(
        self, db: Session, *, owner_id: int, skip: int = 0, limit: int = 100
    ) -> List[Route]:
        return (
            db.query(self.model)
            .filter(Route.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

route = CRUDRoute(Route) 