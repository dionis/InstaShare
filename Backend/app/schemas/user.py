from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    responsability: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

class User(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True
