from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from sqlalchemy.orm import Session

from app.schemas.user import User, UserCreate, Token
from app.core.security import (
    verify_password,
    create_access_token,
) # Ensure get_current_user_email is NOT imported here
from app.core.config import settings
from app.db.session import get_db # Absolute path
from app import crud, models # Import top-level crud and models
from app.api import deps # Import deps

router = APIRouter()

@router.post("/register", response_model=User)
def register_user(user_in: UserCreate, db: Session = Depends(get_db)):
    """Registers a new user in the database."""
    # Correct call via crud module
    db_user = crud.get_user_by_email(db, email=user_in.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    # Correct call via crud module
    created_user = crud.create_user(db=db, user=user_in)
    return created_user

@router.post("/login", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Logs in a user and returns an access token."""
    # Correct call via crud module
    user = crud.get_user_by_email(db, email=form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Use expire time from settings
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/me", response_model=User)
# Correct dependency path
async def read_users_me(current_user: models.User = Depends(deps.get_current_active_user)):
    """Fetches the current logged-in user's data from the database."""
    return current_user 