from db.base import Base
from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

class DocumentStatus(str, enum.Enum):
    uploaded = "uploaded"
    process = "process"
    downloaded = "downloaded"

class Document(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    type = Column(String)
    size = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    status = Column(Enum(DocumentStatus), default=DocumentStatus.uploaded)

    document_shares = relationship("DocumentShared", back_populates="document")








