from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer # Import directly
from sqlalchemy.orm import Session

from app import crud, models # Use absolute imports
# Import settings to get security constants
from app.core.config import settings 
from app.db.session import get_db # Use absolute import
from jose import JWTError, jwt
from typing import Optional

# Define oauth2_scheme here, pointing to the login endpoint
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")

# Dependency to get current user email from token
async def get_current_user_email(token: str = Depends(oauth2_scheme)) -> str:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Use constants from settings
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: Optional[str] = payload.get("sub")
        if email is None:
            raise credentials_exception
        return email
    except JWTError:
        raise credentials_exception

# Dependency to get the full User model from DB based on token
async def get_current_active_user(
    current_email: str = Depends(get_current_user_email),
    db: Session = Depends(get_db)
) -> models.User:
    user = crud.get_user_by_email(db, email=current_email)
    if not user:
        # Changed status code to 401 as invalid token implies unauthorized
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    if not user.is_active:
         raise HTTPException(status_code=400, detail="Inactive user")
    return user 