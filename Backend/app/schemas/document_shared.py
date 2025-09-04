from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class DocumentSharedBase(BaseModel):
    document_id: int
    user_id: int

class DocumentSharedCreate(DocumentSharedBase):
    pass

class DocumentSharedUpdate(DocumentSharedBase):
    document_id: Optional[int] = None
    user_id: Optional[int] = None

class DocumentShared(DocumentSharedBase):
    id: int
    shared_date: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None
    downloaded_at: Optional[datetime] = None

    class Config:
        from_attributes = True
