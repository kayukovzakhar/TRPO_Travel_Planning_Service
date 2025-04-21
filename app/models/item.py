from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, nullable=False)
    completed = Column(Boolean(), default=False)
    checklist_id = Column(Integer, ForeignKey("checklists.id")) # Foreign key to checklists table

    checklist = relationship("Checklist", back_populates="items") # Relationship to parent Checklist 