# backend/models/bookmark.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm    import relationship
from db.base          import Base

class Bookmark(Base):
    __tablename__ = "bookmarks"

    id         = Column(Integer, primary_key=True, index=True)
    user_id    = Column(Integer, ForeignKey("users.id"), nullable=False)
    route_slug = Column(String, nullable=False)

    # связь только с пользователями (никаких back_populates="route" здесь быть не должно!)
    user = relationship("User", back_populates="bookmarks")
