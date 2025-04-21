from pydantic import BaseModel, ConfigDict
from typing import Optional

# Shared properties
class ItemBase(BaseModel):
    description: Optional[str] = None
    completed: Optional[bool] = False

# Properties to receive on item creation
class ItemCreate(ItemBase):
    description: str

# Properties to receive on item update
class ItemUpdate(ItemBase):
    pass

# Properties shared by models stored in DB
class ItemInDBBase(ItemBase):
    id: int
    checklist_id: int

    model_config = ConfigDict(
        from_attributes=True
    )

# Properties to return to client
class Item(ItemInDBBase):
    pass 