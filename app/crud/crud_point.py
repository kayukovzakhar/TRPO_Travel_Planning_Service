from sqlalchemy.orm import Session
from typing import List, Optional

from app.models.point import Point
from app.api.v1.schemas.point import PointCreate, PointUpdate

def get_point(db: Session, point_id: int) -> Optional[Point]:
    """Gets a point by ID."""
    return db.query(Point).filter(Point.id == point_id).first()

def get_points_by_route(db: Session, route_id: int, skip: int = 0, limit: int = 100) -> List[Point]:
    """Gets all points for a specific route."""
    return db.query(Point).filter(Point.route_id == route_id).offset(skip).limit(limit).all()

def create_route_point(db: Session, point: PointCreate, route_id: int) -> Point:
    """Creates a new point associated with a route."""
    db_point = Point(**point.model_dump(), route_id=route_id)
    db.add(db_point)
    db.commit()
    db.refresh(db_point)
    return db_point

def update_point(db: Session, db_point: Point, point_in: PointUpdate) -> Point:
    """Updates an existing point."""
    point_data = point_in.model_dump(exclude_unset=True)
    for key, value in point_data.items():
        setattr(db_point, key, value)
    db.add(db_point)
    db.commit()
    db.refresh(db_point)
    return db_point

def delete_point(db: Session, point_id: int) -> Optional[Point]:
    """Deletes a point by ID."""
    db_point = db.query(Point).filter(Point.id == point_id).first()
    if db_point:
        db.delete(db_point)
        db.commit()
    return db_point 