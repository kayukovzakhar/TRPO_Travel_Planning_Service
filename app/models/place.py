from sqlalchemy import Column, Integer, String, Float, ARRAY, Boolean
from sqlalchemy.orm import relationship

from app.db.base_class import Base

class Place(Base):
    __tablename__ = "places"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    category = Column(String, index=True) # e.g., sight, museum, food, nature, town
    description = Column(String)
    location = Column(String) # Could be address or coordinates
    latitude = Column(Float)  # For geospatial queries
    longitude = Column(Float)  # For geospatial queries
    tags = Column(ARRAY(String))  # For flexible categorization
    rating = Column(Float)  # Average rating
    price_level = Column(Integer)  # 1-5 scale for price level
    is_active = Column(Boolean, default=True)  # For soft deletion
    opening_hours = Column(String)  # Store as JSON string
    contact_info = Column(String)  # Store as JSON string
    image_url = Column(String)  # URL to the main image
    website = Column(String)  # Official website if available
    # Add region/city later if needed for multiple destinations
    # region = Column(String, index=True, default="Kaliningrad") 