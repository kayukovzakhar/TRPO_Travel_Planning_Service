from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base # Use absolute import

class Point(Base):
    __tablename__ = "points"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    location = Column(String) # Could be coordinates, address, etc.
    visited = Column(Boolean(), default=False)
    route_id = Column(Integer, ForeignKey("routes.id")) # Foreign key to routes table

    route = relationship("Route", back_populates="points") # Relationship to parent Route 