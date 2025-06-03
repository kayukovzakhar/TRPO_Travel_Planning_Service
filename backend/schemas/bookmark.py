from pydantic import BaseModel

class BookmarkCreate(BaseModel):
    route_slug: str

class BookmarkResponse(BaseModel):
    id:         int
    user_id:    int
    route_slug: str

    class Config:
        orm_mode = True
