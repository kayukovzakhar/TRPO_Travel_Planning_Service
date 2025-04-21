from pydantic import BaseModel, ConfigDict
from typing import List, Optional

# Import Item schema
from .item import Item

# Shared properties (currently none specific to checklist itself)
class ChecklistBase(BaseModel):
    pass

# Properties to receive on creation (usually created automatically with Route)
class ChecklistCreate(ChecklistBase):
    pass

# Properties to receive on update (maybe update status or name in future?)
class ChecklistUpdate(ChecklistBase):
    pass

# Properties shared by models stored in DB
class ChecklistInDBBase(ChecklistBase):
    id: int
    route_id: int

    model_config = ConfigDict(
        from_attributes=True
    )

# Properties to return to client
class Checklist(ChecklistInDBBase):
    items: List[Item] = [] 