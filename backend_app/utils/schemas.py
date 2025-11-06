from pydantic import BaseModel, EmailStr
from typing import Optional

# Public user data
class UserOut(BaseModel):
    id: int
    email: EmailStr
    full_name: Optional[str] = None
    is_active: bool

    class Config:
        from_attributes = True


# For creating a user
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str] = None

# For login
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    user_id: Optional[int] = None
