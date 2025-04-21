from pydantic import BaseModel
from typing import Optional

class Place(BaseModel):
    id: int
    name: str
    category: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None 