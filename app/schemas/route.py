from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

class RouteBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    start_location: str = Field(..., min_length=1, max_length=100)
    end_location: str = Field(..., min_length=1, max_length=100)
    places: List[int] = Field(default_factory=list)  # List of place IDs
    duration: Optional[int] = Field(None, ge=0)  # Duration in minutes
    distance: Optional[float] = Field(None, ge=0)  # Distance in kilometers
    is_public: bool = Field(default=True)
    tags: List[str] = Field(default_factory=list)

class RouteCreate(RouteBase):
    pass

class RouteUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    start_location: Optional[str] = Field(None, min_length=1, max_length=100)
    end_location: Optional[str] = Field(None, min_length=1, max_length=100)
    places: Optional[List[int]] = None
    duration: Optional[int] = Field(None, ge=0)
    distance: Optional[float] = Field(None, ge=0)
    is_public: Optional[bool] = None
    tags: Optional[List[str]] = None

class RouteInDB(RouteBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class Route(RouteInDB):
    pass 