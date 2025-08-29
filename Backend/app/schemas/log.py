from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class LogBase(BaseModel):
    event: str
    user_id: int
    event_description: Optional[str] = None

class LogCreate(LogBase):
    pass

class LogUpdate(LogBase):
    event: Optional[str] = None
    user_id: Optional[int] = None
    event_description: Optional[str] = None

class Log(LogBase):
    id: int
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True
