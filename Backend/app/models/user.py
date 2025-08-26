from db.base import Base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    password = Column(String)
    email = Column(String, unique=True, index=True)
    phone = Column(String, nullable=True)
    responsability = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)

    user_roles = relationship("UserRole", back_populates="user")
    documents_shared = relationship("DocumentShared", back_populates="user")
    logs = relationship("Log", back_populates="user")
