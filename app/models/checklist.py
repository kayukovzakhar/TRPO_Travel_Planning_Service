from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base

class Checklist(Base):
    __tablename__ = "checklists"

    id = Column(Integer, primary_key=True, index=True)
    # One-to-one relationship with Route: Each route has one checklist
    route_id = Column(Integer, ForeignKey("routes.id"), unique=True)

    # Relationship back to the Route
    route = relationship("Route", back_populates="checklist")

    # Relationship to Items
    items = relationship("Item", back_populates="checklist", cascade="all, delete-orphan", lazy="selectin") 