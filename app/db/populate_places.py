import logging
import sys
import os

# Add project root to sys.path to allow absolute imports when run directly
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from app.db.session import SessionLocal
from app.crud import create_place, get_places
from app.core.suggested_places import SUGGESTED_PLACES_KALININGRAD

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def populate_places() -> None:
    db = SessionLocal()
    try:
        existing_places = get_places(db, limit=1) # Check if places already exist
        if existing_places:
            logger.info("Places table already populated. Skipping.")
            return
        
        logger.info("Populating places table...")
        for place_data in SUGGESTED_PLACES_KALININGRAD:
            try:
                # We are using the dict directly, including the 'id' from the static list
                create_place(db=db, place_data=place_data)
                logger.info(f"Created place: {place_data.get('name')}")
            except Exception as e:
                logger.error(f"Error creating place {place_data.get('name')}: {e}")
                # Optionally rollback or handle the error
                # db.rollback()
        logger.info("Places table populated successfully.")
    finally:
        db.close()

def main() -> None:
    logger.info("Starting places population script...")
    populate_places()
    logger.info("Places population script finished.")

if __name__ == "__main__":
    main() 