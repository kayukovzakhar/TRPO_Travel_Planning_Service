from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean(), default=True) # Added is_active field

    # Relationship to Routes
    # user.routes will give a list of routes owned by the user
    routes = relationship("Route", back_populates="owner", cascade="all, delete-orphan")

    # Relationships (we will define Route model later)
    # routes = relationship("Route", back_populates="owner") 