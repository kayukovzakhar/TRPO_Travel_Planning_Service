from sqlalchemy import Column, String, Text
from db.base import Base

class Route(Base):
    __tablename__ = "routes"

    slug        = Column(String, primary_key=True, index=True)
    title       = Column(String, nullable=False)
    description = Column(Text, nullable=True)

    # УДАЛИть или закомментировать
    # bookmarks = relationship("Bookmark", back_populates="route", cascade="all, delete-orphan")
