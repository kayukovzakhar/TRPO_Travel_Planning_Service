from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

from app.models.place import Place
# We might need schemas later for creating/updating places via API
# from app.api.v1.schemas.place import PlaceCreate, PlaceUpdate 

def get_place(db: Session, place_id: int) -> Optional[Place]:
    """Gets a place by ID."""
    return db.query(Place).filter(Place.id == place_id).first()

def get_places(db: Session, skip: int = 0, limit: int = 100) -> List[Place]:
    """Gets all places (e.g., for suggestions)."""
    return db.query(Place).offset(skip).limit(limit).all()

# Function to create a place (needed for population script)
def create_place(db: Session, place_data: dict) -> Place:
    """Creates a new place. Expects a dictionary with place data."""
    # Ensure ID is not passed if it's auto-generated or handled differently
    # place_data.pop('id', None) 
    db_place = Place(**place_data)
    db.add(db_place)
    db.commit()
    db.refresh(db_place)
    return db_place

# Add update/delete later if needed 

from app.crud.base import CRUDBase
from app.schemas.place import PlaceCreate, PlaceUpdate

class CRUDPlace(CRUDBase[Place, PlaceCreate, PlaceUpdate]):
    def get_by_name(self, db: Session, *, name: str) -> Optional[Place]:
        return db.query(Place).filter(Place.name == name).first()

    def get_multi(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100,
        category: Optional[str] = None,
        tags: Optional[List[str]] = None,
        min_rating: Optional[float] = None,
        max_price: Optional[int] = None,
        search: Optional[str] = None
    ) -> List[Place]:
        query = db.query(Place).filter(Place.is_active == True)
        
        if category:
            query = query.filter(Place.category == category)
        
        if tags:
            query = query.filter(Place.tags.overlap(tags))
        
        if min_rating:
            query = query.filter(Place.rating >= min_rating)
        
        if max_price:
            query = query.filter(Place.price_level <= max_price)
        
        if search:
            search_filter = or_(
                Place.name.ilike(f"%{search}%"),
                Place.description.ilike(f"%{search}%"),
                Place.location.ilike(f"%{search}%")
            )
            query = query.filter(search_filter)
        
        return query.offset(skip).limit(limit).all()

    def get_nearby(
        self,
        db: Session,
        *,
        latitude: float,
        longitude: float,
        radius: float = 5.0,
        limit: int = 50
    ) -> List[Place]:
        # Simple distance calculation (for small distances)
        # For production, consider using PostGIS or similar
        query = db.query(Place).filter(Place.is_active == True)
        places = query.all()
        
        nearby_places = []
        for place in places:
            if place.latitude and place.longitude:
                # Calculate distance using Haversine formula
                from math import radians, sin, cos, sqrt, atan2
                R = 6371  # Earth's radius in km
                
                lat1, lon1 = radians(latitude), radians(longitude)
                lat2, lon2 = radians(place.latitude), radians(place.longitude)
                
                dlat = lat2 - lat1
                dlon = lon2 - lon1
                
                a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
                c = 2 * atan2(sqrt(a), sqrt(1-a))
                distance = R * c
                
                if distance <= radius:
                    nearby_places.append(place)
        
        return nearby_places[:limit]

place = CRUDPlace(Place) 