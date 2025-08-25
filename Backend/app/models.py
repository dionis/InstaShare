
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

Base = declarative_base()

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

class DocumentStatus(str, enum.Enum):
    uploaded = "uploaded"
    process = "process"
    downloaded = "downloaded"

class Document(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    type = Column(String)
    size = Column(String, nullable=True) # Storing as string for "456M" or "7Gb"
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    status = Column(Enum(DocumentStatus), default=DocumentStatus.uploaded)

    document_shares = relationship("DocumentShared", back_populates="document")

class Role(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, index=True)
    role_name = Column(String, unique=True, index=True)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow) # Changed from uploaded_at to created_at for logical consistency
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)

    user_roles = relationship("UserRole", back_populates="role")

class DocumentShared(Base):
    __tablename__ = "documents_shared"
    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    shared_date = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)
    downloaded_at = Column(DateTime, nullable=True) # Corrected from donwloaded_at

    document = relationship("Document", back_populates="document_shares")
    user = relationship("User", back_populates="documents_shared")

class UserRole(Base):
    __tablename__ = "user_roles"
    id = Column(Integer, primary_key=True, index=True)
    role_id = Column(Integer, ForeignKey("roles.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    assigned_date = Column(DateTime, default=datetime.utcnow) # Changed from shared_date to assigned_date
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)

    role = relationship("Role", back_populates="user_roles")
    user = relationship("User", back_populates="user_roles")

class Log(Base):
    __tablename__ = "logs"
    id = Column(Integer, primary_key=True, index=True)
    event = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    event_description = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow) # Changed from shared_date to created_at
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="logs")
