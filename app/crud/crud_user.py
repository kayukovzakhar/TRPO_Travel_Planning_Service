from sqlalchemy.orm import Session
from typing import Optional

from app.core.security import get_password_hash
from app.models.user import User
from app.api.v1.schemas.user import UserCreate # Use the schema for creation

def get_user(db: Session, user_id: int) -> Optional[User]:
    """Gets a user by ID."""
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """Gets a user by email."""
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user: UserCreate) -> User:
    """Creates a new user."""
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        name=user.name,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Add other CRUD operations as needed (update, delete, get multiple users, etc.) 