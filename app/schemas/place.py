from typing import List, Optional
from pydantic import BaseModel, Field, field_validator, ConfigDict

class PlaceBase(BaseModel):
    name: str
    description: Optional[str] = None
    location: str
    category: str
    tags: List[str] = Field(default_factory=list)
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    rating: Optional[float] = Field(None, ge=0, le=5)
    price_level: Optional[int] = Field(None, ge=1, le=4)
    opening_hours: Optional[str] = None
    contact_info: Optional[str] = None
    image_url: Optional[str] = None
    website: Optional[str] = None

    @field_validator('latitude')
    @classmethod
    def validate_latitude(cls, v):
        if v is not None and (v < -90 or v > 90):
            raise ValueError('Latitude must be between -90 and 90')
        return v

    @field_validator('longitude')
    @classmethod
    def validate_longitude(cls, v):
        if v is not None and (v < -180 or v > 180):
            raise ValueError('Longitude must be between -180 and 180')
        return v

class PlaceCreate(PlaceBase):
    pass

class PlaceUpdate(PlaceBase):
    name: Optional[str] = None
    location: Optional[str] = None
    category: Optional[str] = None
    is_active: Optional[bool] = None

class PlaceInDB(PlaceBase):
    id: int
    is_active: bool = True

    model_config = ConfigDict(from_attributes=True)

class Place(PlaceInDB):
    pass 