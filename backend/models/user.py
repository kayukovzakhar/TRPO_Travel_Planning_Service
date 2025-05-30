from sqlalchemy import Column, Integer, String  # или другие нужные типы
from sqlalchemy.orm import relationship
from db.base import Base
from sqlalchemy.types import Boolean

    
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

    # связь к закладкам (если вы её завели)
    bookmarks = relationship(
        "Bookmark", 
        back_populates="user", 
        cascade="all, delete-orphan"
    )
