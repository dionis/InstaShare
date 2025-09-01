from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field

class UserBase(BaseModel):
    username:  Optional[str] = None
    email: EmailStr
    phone: Optional[str] = None
    responsability: Optional[str] = None
    
   

class UserCreate(UserBase):
    password: str # Plain password for Supabase auth
    hashed_password: Optional[str] = None # Hashed password to store in your database

class UserUpdate(UserBase):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

class User(UserBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    

    role:  Optional[str] = None
    hashed_password: Optional[str] = None

    class Config:
        from_attributes = True
