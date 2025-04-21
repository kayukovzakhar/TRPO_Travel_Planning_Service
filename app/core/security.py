from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from typing import Optional

from jose import JWTError, jwt
# Remove Depends, HTTPException, status, OAuth2PasswordBearer as they are now handled in deps.py
# from fastapi import Depends, HTTPException, status
# from fastapi.security import OAuth2PasswordBearer

# Import settings for security constants
from app.core.config import settings 

# --- Remove JWT Configuration Constants --- 
# SECRET_KEY = "your-super-secret-key"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Remove oauth2_scheme definition, it's in deps.py now
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")
# --- End JWT Configuration ---

# Setup password hashing context using bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a plain password against a hashed password."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hashes a plain password."""
    return pwd_context.hash(password)

# --- JWT Token Functions ---
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        # Use expiration time from settings
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    # Use constants from settings
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

# Remove get_current_user_email and get_current_active_user definitions
# async def get_current_user_email(token: str = Depends(oauth2_scheme)) -> str:
#     ...

# async def get_current_active_user(current_email: str = Depends(get_current_user_email)):
#     ...
# --- End JWT Token Functions ---

# Placeholder for JWT token functions (to be implemented later)
# def create_access_token(data: dict, expires_delta: timedelta = None):
#     pass

# def decode_access_token(token: str):
#     pass 