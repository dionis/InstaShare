from db.base import Base
from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

class DocumentShared(Base):
    __tablename__ = "documents_shared"
    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    shared_date = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)
    downloaded_at = Column(DateTime, nullable=True)

    document = relationship("Document", back_populates="document_shares")
    user = relationship("User", back_populates="documents_shared")






