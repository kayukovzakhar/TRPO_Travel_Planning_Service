from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import List, Optional

# Schema for user registration request
class UserCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=8)

# Schema for user login request
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Base schema for user data (used for responses)
class UserBase(BaseModel):
    id: int
    name: str
    email: EmailStr

# Schema for user response (excluding sensitive info like password)
class User(UserBase):
    # We might add other fields like is_active, routes later
    pass

    model_config = ConfigDict(
        from_attributes=True
    )

# Schema for token response
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None 