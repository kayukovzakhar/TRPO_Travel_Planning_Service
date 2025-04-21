from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Any

from app import crud, models # Import top-level crud, models
from app.api.v1 import schemas # Import schemas from correct path
from app.api import deps # We will create this dependency file
from app.db.session import get_db # Use absolute import

router = APIRouter()

@router.post("/", response_model=schemas.Route)
def create_route(
    *, # Enforces keyword-only arguments after this
    db: Session = Depends(get_db),
    route_in: schemas.RouteCreate,
    current_user: models.User = Depends(deps.get_current_active_user) # Ensure user is logged in
) -> Any:
    """Create new route for the current user."""
    route = crud.create_owner_route(db=db, route=route_in, owner_id=current_user.id)
    return route

@router.get("/", response_model=List[schemas.Route])
def read_routes(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user)
) -> Any:
    """Retrieve routes owned by the current user."""
    routes = crud.get_routes_by_owner(db, owner_id=current_user.id, skip=skip, limit=limit)
    return routes

@router.get("/{route_id}", response_model=schemas.Route)
def read_route(
    *, 
    db: Session = Depends(get_db),
    route_id: int,
    current_user: models.User = Depends(deps.get_current_active_user)
) -> Any:
    """Get specific route by ID owned by the current user."""
    route = crud.get_route(db, route_id=route_id)
    if not route:
        raise HTTPException(status_code=404, detail="Route not found")
    if route.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    return route

@router.put("/{route_id}", response_model=schemas.Route)
def update_route(
    *,
    db: Session = Depends(get_db),
    route_id: int,
    route_in: schemas.RouteUpdate,
    current_user: models.User = Depends(deps.get_current_active_user)
) -> Any:
    """Update a route owned by the current user."""
    route = crud.get_route(db, route_id=route_id)
    if not route:
        raise HTTPException(status_code=404, detail="Route not found")
    if route.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    route = crud.update_route(db=db, db_route=route, route_in=route_in)
    return route

@router.delete("/{route_id}", response_model=schemas.Route)
def delete_route(
    *,
    db: Session = Depends(get_db),
    route_id: int,
    current_user: models.User = Depends(deps.get_current_active_user)
) -> Any:
    """Delete a route owned by the current user."""
    route = crud.get_route(db, route_id=route_id)
    if not route:
        raise HTTPException(status_code=404, detail="Route not found")
    if route.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    deleted_route = crud.delete_route(db=db, route_id=route_id)
    return deleted_route

# --- Point Endpoints (nested under routes) ---
# We can add endpoints for adding/updating/deleting points within a specific route here
# Example: POST /routes/{route_id}/points/

@router.post("/{route_id}/points/", response_model=schemas.Point)
def create_point_for_route(
    *,
    db: Session = Depends(get_db),
    route_id: int,
    point_in: schemas.PointCreate,
    current_user: models.User = Depends(deps.get_current_active_user)
) -> Any:
    """Create a new point within a specific route owned by the current user."""
    route = crud.get_route(db, route_id=route_id)
    if not route:
        raise HTTPException(status_code=404, detail="Route not found")
    if route.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    point = crud.create_route_point(db=db, point=point_in, route_id=route_id)
    return point

# Add PUT/DELETE for points if needed

@router.put("/{route_id}/points/{point_id}", response_model=schemas.Point)
def update_route_point(
    route_id: int,
    point_id: int,
    *,
    point_in: schemas.PointUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(deps.get_current_active_user) # Verify user
) -> Any:
    """Update a point within a specific route owned by the current user."""
    # Verify route ownership
    route = crud.get_route(db, route_id=route_id)
    if not route:
        raise HTTPException(status_code=404, detail="Route not found")
    if route.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions for route")

    # Get the specific point and verify it belongs to the route
    db_point = crud.get_point(db, point_id=point_id)
    if not db_point or db_point.route_id != route_id:
        raise HTTPException(status_code=404, detail="Point not found in this route")

    # Update the point
    updated_point = crud.update_point(db=db, db_point=db_point, point_in=point_in)
    return updated_point

# Add PUT/DELETE for points if needed - Placeholder for DELETE
@router.delete("/{route_id}/points/{point_id}", response_model=schemas.Point)
def delete_route_point(
    route_id: int,
    point_id: int,
    *,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(deps.get_current_active_user) # Verify user
) -> Any:
    """Delete a point from a specific route owned by the current user."""
    # Verify route ownership
    route = crud.get_route(db, route_id=route_id)
    if not route:
        raise HTTPException(status_code=404, detail="Route not found")
    if route.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions for route")

    # Get the specific point and verify it belongs to the route
    db_point = crud.get_point(db, point_id=point_id)
    if not db_point or db_point.route_id != route_id:
        raise HTTPException(status_code=404, detail="Point not found in this route")

    # Delete the point
    deleted_point = crud.delete_point(db=db, point_id=point_id)
    if not deleted_point:
         raise HTTPException(status_code=404, detail="Point not found or already deleted") 
    return deleted_point 