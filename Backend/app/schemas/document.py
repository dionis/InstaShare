from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from enum import Enum

class DocumentStatusSchema(str, Enum):
    uploaded = "uploaded"
    process = "process"
    downloaded = "downloaded"

class DocumentBase(BaseModel):
    name: str
    type: str
    size: Optional[str] = None
    status: DocumentStatusSchema = DocumentStatusSchema.uploaded
    file_url: Optional[str] = None

class DocumentCreate(DocumentBase):
    pass

class DocumentUpdate(DocumentBase):
    name: Optional[str] = None
    type: Optional[str] = None
    size: Optional[str] = None
    status: Optional[DocumentStatusSchema] = None

class Document(DocumentBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    uploaded_at: Optional[datetime] = None


    class Config:
        from_attributes = True
