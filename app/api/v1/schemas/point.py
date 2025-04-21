from pydantic import BaseModel, ConfigDict
from typing import Optional

# Properties shared by models stored in DB
class PointBase(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None
    visited: Optional[bool] = False

# Properties to receive via API on creation
class PointCreate(PointBase):
    name: str
    # route_id will be set based on the route endpoint

# Properties to receive via API on update
class PointUpdate(PointBase):
    pass

# Properties stored in DB
class PointInDBBase(PointBase):
    id: int
    route_id: int

    model_config = ConfigDict(
        from_attributes=True
    )

# Additional properties to return via API
class Point(PointInDBBase):
    pass 