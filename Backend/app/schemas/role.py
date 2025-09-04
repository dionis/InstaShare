from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class RoleBase(BaseModel):
    role_name: str
    description: Optional[str] = None

class RoleCreate(RoleBase):
    pass

class RoleUpdate(RoleBase):
    role_name: Optional[str] = None
    description: Optional[str] = None

class Role(RoleBase):
    id: int
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True
