from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class UserRoleBase(BaseModel):
    role_id: int
    user_id: int

class UserRoleCreate(UserRoleBase):
    pass

class UserRoleUpdate(UserRoleBase):
    role_id: Optional[int] = None
    user_id: Optional[int] = None

class UserRole(UserRoleBase):
    id: int
    assigned_date: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True
