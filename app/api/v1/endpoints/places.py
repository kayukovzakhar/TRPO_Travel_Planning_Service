from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app import crud
from app.api import deps
from app.schemas import Place, PlaceCreate, PlaceUpdate

router = APIRouter()

@router.get("/", response_model=List[Place])
def read_places(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    category: Optional[str] = None,
    tags: Optional[List[str]] = Query(None),
    min_rating: Optional[float] = None,
    max_price: Optional[int] = None,
    search: Optional[str] = None,
):
    """
    Retrieve places with optional filtering and search.
    """
    places = crud.place.get_multi(
        db,
        skip=skip,
        limit=limit,
        category=category,
        tags=tags,
        min_rating=min_rating,
        max_price=max_price,
        search=search,
    )
    return places

@router.post("/", response_model=Place)
def create_place(
    *,
    db: Session = Depends(deps.get_db),
    place_in: PlaceCreate,
):
    """
    Create new place.
    """
    place = crud.place.get_by_name(db, name=place_in.name)
    if place:
        raise HTTPException(
            status_code=400,
            detail="A place with this name already exists.",
        )
    place = crud.place.create(db, obj_in=place_in)
    return place

@router.get("/{place_id}", response_model=Place)
def read_place(
    *,
    db: Session = Depends(deps.get_db),
    place_id: int,
):
    """
    Get place by ID.
    """
    place = crud.place.get(db, id=place_id)
    if not place:
        raise HTTPException(
            status_code=404,
            detail="Place not found",
        )
    return place

@router.put("/{place_id}", response_model=Place)
def update_place(
    *,
    db: Session = Depends(deps.get_db),
    place_id: int,
    place_in: PlaceUpdate,
):
    """
    Update place.
    """
    place = crud.place.get(db, id=place_id)
    if not place:
        raise HTTPException(
            status_code=404,
            detail="Place not found",
        )
    place = crud.place.update(db, db_obj=place, obj_in=place_in)
    return place

@router.delete("/{place_id}", response_model=Place)
def delete_place(
    *,
    db: Session = Depends(deps.get_db),
    place_id: int,
):
    """
    Delete place.
    """
    place = crud.place.get(db, id=place_id)
    if not place:
        raise HTTPException(
            status_code=404,
            detail="Place not found",
        )
    place = crud.place.remove(db, id=place_id)
    return place

@router.get("/nearby/", response_model=List[Place])
def get_nearby_places(
    *,
    db: Session = Depends(deps.get_db),
    latitude: float = Query(..., description="Latitude of the center point"),
    longitude: float = Query(..., description="Longitude of the center point"),
    radius: float = Query(5.0, description="Search radius in kilometers"),
    limit: int = 100,
):
    """
    Get places within a specified radius of given coordinates.
    """
    places = crud.place.get_nearby(
        db,
        latitude=latitude,
        longitude=longitude,
        radius=radius,
        limit=limit,
    )
    return places

# Add more endpoints later, e.g., search places, get place details 