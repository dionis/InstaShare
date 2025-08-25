
from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel, Relationship
import enum


class User(SQLModel, table=True):
    __tablename__ = "users"
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    password: str
    email: str = Field(unique=True, index=True)
    phone: Optional[str] = None
    responsability: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column_kwargs={"onupdate": datetime.utcnow})
    deleted_at: Optional[datetime] = None
    role: Optional[str] = None # Added for user role representation

    user_roles: list["UserRole"] = Relationship(back_populates="user")
    documents_shared: list["DocumentShared"] = Relationship(back_populates="user")
    logs: list["Log"] = Relationship(back_populates="user")


class DocumentStatus(str, enum.Enum):
    uploaded = "uploaded"
    process = "process"
    downloaded = "downloaded"


class Document(SQLModel, table=True):
    __tablename__ = "documents"
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    type: str
    size: Optional[str] = None  # Storing as string for "456M" or "7Gb"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column_kwargs={"onupdate": datetime.utcnow})
    deleted_at: Optional[datetime] = None
    uploaded_at: datetime = Field(default_factory=datetime.utcnow)
    status: DocumentStatus = Field(default=DocumentStatus.uploaded)

    document_shares: list["DocumentShared"] = Relationship(back_populates="document")


class Role(SQLModel, table=True):
    __tablename__ = "roles"
    id: Optional[int] = Field(default=None, primary_key=True)
    role_name: str = Field(unique=True, index=True)
    description: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column_kwargs={"onupdate": datetime.utcnow})
    deleted_at: Optional[datetime] = None

    user_roles: list["UserRole"] = Relationship(back_populates="role")


class DocumentShared(SQLModel, table=True):
    __tablename__ = "documents_shared"
    id: Optional[int] = Field(default=None, primary_key=True)
    document_id: Optional[int] = Field(default=None, foreign_key="documents.id")
    user_id: Optional[int] = Field(default=None, foreign_key="users.id")
    shared_date: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column_kwargs={"onupdate": datetime.utcnow})
    deleted_at: Optional[datetime] = None
    uploaded_at: datetime = Field(default_factory=datetime.utcnow)
    downloaded_at: Optional[datetime] = None

    document: Optional[Document] = Relationship(back_populates="document_shares")
    user: Optional[User] = Relationship(back_populates="documents_shared")


class UserCreate(SQLModel):
    name: str
    password: str
    email: str
    phone: Optional[str] = None
    responsability: Optional[str] = None


class UserUpdate(SQLModel):
    name: Optional[str] = None
    password: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    responsability: Optional[str] = None


class DocumentCreate(SQLModel):
    name: str
    type: str
    size: Optional[str] = None
    status: Optional[DocumentStatus] = None


class DocumentUpdate(SQLModel):
    name: Optional[str] = None
    type: Optional[str] = None
    size: Optional[str] = None
    status: Optional[DocumentStatus] = None


class RoleCreate(SQLModel):
    role_name: str
    description: Optional[str] = None


class RoleUpdate(SQLModel):
    role_name: Optional[str] = None
    description: Optional[str] = None


class UserRole(SQLModel, table=True):
    __tablename__ = "user_roles"
    id: Optional[int] = Field(default=None, primary_key=True)
    role_id: Optional[int] = Field(default=None, foreign_key="roles.id")
    user_id: Optional[int] = Field(default=None, foreign_key="users.id")
    assigned_date: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column_kwargs={"onupdate": datetime.utcnow})
    deleted_at: Optional[datetime] = None
    uploaded_at: datetime = Field(default_factory=datetime.utcnow)

    role: Optional[Role] = Relationship(back_populates="user_roles")
    user: Optional[User] = Relationship(back_populates="user_roles")


class Log(SQLModel, table=True):
    __tablename__ = "logs"
    id: Optional[int] = Field(default=None, primary_key=True)
    event: str
    user_id: Optional[int] = Field(default=None, foreign_key="users.id")
    event_description: Optional[str] = None
    shared_date: datetime = Field(default_factory=datetime.utcnow) # This might be renamed to 'event_date' for clarity if needed
    updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column_kwargs={"onupdate": datetime.utcnow})
    deleted_at: Optional[datetime] = None
    uploaded_at: datetime = Field(default_factory=datetime.utcnow)

    user: Optional[User] = Relationship(back_populates="logs")
