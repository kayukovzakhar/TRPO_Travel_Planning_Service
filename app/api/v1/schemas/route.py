from pydantic import BaseModel, ConfigDict
from typing import List, Optional

# Import Point schema using absolute path
from app.api.v1.schemas.point import Point, PointCreate
# Import Checklist schema
from .checklist import Checklist

# Properties shared by models stored in DB
class RouteBase(BaseModel):
    name: Optional[str] = None

# Properties to receive via API on creation
# Can optionally include points during creation
class RouteCreate(RouteBase):
    name: str
    points: Optional[List[PointCreate]] = [] # Allow creating points along with route

# Properties to receive via API on update
class RouteUpdate(RouteBase):
    pass

# Properties stored in DB
class RouteInDBBase(RouteBase):
    id: int
    owner_id: int

    model_config = ConfigDict(
        from_attributes=True
    )

# Additional properties to return via API
# Includes the list of points associated with the route
class Route(RouteInDBBase):
    points: List[Point] = []
    checklist: Optional[Checklist] = None # Add checklist field 