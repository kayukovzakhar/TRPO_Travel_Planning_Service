from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base # Use absolute import

class Route(Base):
    __tablename__ = "routes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id")) # Foreign key to users table

    # Relationship to User (owner)
    owner = relationship("User", back_populates="routes")
    # Relationship to Points (list of points in the route)
    # cascade="all, delete-orphan" means points are deleted when the route is deleted
    points = relationship("Point", back_populates="route", cascade="all, delete-orphan", lazy="selectin")

    # Relationship to Checklist (one-to-one)
    checklist = relationship("Checklist", uselist=False, back_populates="route", cascade="all, delete-orphan") 