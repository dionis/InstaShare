import os
from fastapi import FastAPI, Depends, HTTPException, status, UploadFile, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware

from core.config import Settings
from db.base import get_db, SessionLocal, Base, engine, get_supabase_client
from db.seed import create_initial_data
from db.clean import clean_db_tables
from auth.jwt import create_access_token, Token
from auth.dependencies import get_current_user

from schemas.user import User, UserCreate, UserUpdate
from schemas.document import Document, DocumentCreate, DocumentUpdate
from schemas.role import Role, RoleCreate, RoleUpdate
from schemas.log import LogBase, Log, LogCreate, LogUpdate
from schemas.document_shared import DocumentShared, DocumentSharedCreate, DocumentSharedUpdate
from schemas.user_role import UserRole, UserRoleCreate, UserRoleUpdate

from models.user import User as UserModel # To query user for authentication

from services.document_service import DocumentService
from services.user_service import UserService
from services.role_service import RoleService
from services.log_service import LogService
from typing import List, Optional
from sqlalchemy.orm import Session
from supabase import Client

from celery import Celery
from celery.schedules import crontab
from datetime import date


settings = Settings()


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
)

app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],  # Allows all HTTP methods (GET, POST, PUT, DELETE, etc.)
        allow_headers=["*"],  # Allows all headers
    )


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        if os.getenv("DEVELOPMENT_SUPPORT"):
          create_initial_data(db)
    finally:
        db.close()
        
@app.on_event("shutdown")
async def shutdown_event():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
       ##clean  all temporal values if was created 
       if os.getenv("DEVELOPMENT_SUPPORT"):
         clean_db_tables(db)
    finally:
        db.close()

@app.get("/", tags=["Health Check"])
async def read_root():
    return {"message": "Welcome to InstaShare Backend!"}

@app.get("/health", tags=["Health Check"])
async def health_check():
    return {
        "status": "ok",
        "service_name": settings.PROJECT_NAME,
        "version": settings.PROJECT_VERSION,
    }

# New Token Endpoint
@app.post("/token", response_model=Token, tags=["Authentication"])
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.email == form_data.username).first()
    if not user or user.password != form_data.password: # In a real app, hash and verify passwords
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

###---  Main app services ------------------------------------------------------------

# Dependency to get DocumentService
async def get_document_service(supabase: Client = Depends(get_supabase_client)) -> DocumentService:
    return DocumentService(supabase)

# Dependency to get UserService
async def get_user_service(supabase: Client = Depends(get_supabase_client)) -> UserService:
    return UserService(supabase)

# Dependency to get RoleService
async def get_role_service(supabase: Client = Depends(get_supabase_client)) -> RoleService:
    return RoleService(supabase)

# Dependency to get LogService
async def get_log_service(supabase: Client = Depends(get_supabase_client)) -> LogService:
    return LogService(supabase)

# Document Endpoints
@app.post("/documents/upload_document/{document_id}", response_model=Document)
async def upload_document_info(document_id: int, document: DocumentCreate, document_service: DocumentService = Depends(get_document_service)):
    try:
        created_document = await document_service.upload_document_info(document_id, document)
        return created_document
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.post("/documents/authenticated/upload_document/{document_id}", response_model=Document, tags=["Documents", "Authenticated"])
async def upload_document_info_authenticated(document_id: int, document: DocumentCreate, document_service: DocumentService = Depends(get_document_service), current_user: User = Depends(get_current_user)):
    try:
        created_document = await document_service.upload_document_info(document_id, document)
        return created_document
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.post("/documents/upload_document_file/{document_id}", response_model=Document)
async def upload_document_file(document_id: int, file: UploadFile, document_service: DocumentService = Depends(get_document_service)):
    try:
        updated_document = await document_service.upload_document_file(document_id, file)
        return updated_document
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.post("/documents/authenticated/upload_document_file/{document_id}", response_model=Document, tags=["Documents", "Authenticated"])
async def upload_document_file_authenticated(document_id: int, file: UploadFile, document_service: DocumentService = Depends(get_document_service), current_user: User = Depends(get_current_user)):
    try:
        updated_document = await document_service.upload_document_file(document_id, file)
        return updated_document
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.delete("/documents/{document_id}", response_model=dict)
async def delete_document(document_id: int, document_service: DocumentService = Depends(get_document_service)):
    try:
        result = await document_service.delete_document(document_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.delete("/documents/authenticated/{document_id}", response_model=dict, tags=["Documents", "Authenticated"])
async def delete_document_authenticated(document_id: int, document_service: DocumentService = Depends(get_document_service), current_user: User = Depends(get_current_user)):
    try:
        result = await document_service.delete_document(document_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.put("/documents/{document_id}", response_model=Document)
async def update_document_info(document_id: int, document: DocumentUpdate, document_service: DocumentService = Depends(get_document_service)):
    try:
        updated_document = await document_service.update_document_info(document_id, document)
        if not updated_document:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")
        return updated_document
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.put("/documents/authenticated/{document_id}", response_model=Document, tags=["Documents", "Authenticated"])
async def update_document_info_authenticated(document_id: int, document: DocumentUpdate, document_service: DocumentService = Depends(get_document_service), current_user: User = Depends(get_current_user)):
    try:
        updated_document = await document_service.update_document_info(document_id, document)
        if not updated_document:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")
        return updated_document
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.get("/documents/", response_model=List[Document])
async def list_all_documents(document_service: DocumentService = Depends(get_document_service)):
    try:
        documents = await document_service.list_documents()
        return documents
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.get("/documents/authenticated/", response_model=List[Document], tags=["Documents", "Authenticated"])
async def list_all_documents_authenticated(document_service: DocumentService = Depends(get_document_service), current_user: User = Depends(get_current_user)):
    try:
        documents = await document_service.list_documents()
        return documents
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.get("/documents/{document_id}", response_model=Document)
async def get_document_by_id(document_id: int, document_service: DocumentService = Depends(get_document_service)):
    try:
        document = await document_service.get_document(document_id)
        if not document:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")
        return document
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.get("/documents/authenticated/{document_id}", response_model=Document, tags=["Documents", "Authenticated"])
async def get_document_by_id_authenticated(document_id: int, document_service: DocumentService = Depends(get_document_service), current_user: User = Depends(get_current_user)):
    try:
        document = await document_service.get_document(document_id)
        if not document:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")
        return document
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.get("/documents/{document_id}/shared_by/users", response_model=List[User])
async def get_document_shared_users(document_id: int, document_service: DocumentService = Depends(get_document_service)):
    try:
        shared_info = await document_service.get_shared_users_for_document(document_id)
        if not shared_info:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found or not shared with any users")
        return shared_info
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.get("/documents/authenticated/{document_id}/shared_by/users", response_model=List[User], tags=["Documents", "Authenticated"])
async def get_document_shared_users_authenticated(document_id: int, document_service: DocumentService = Depends(get_document_service), current_user: User = Depends(get_current_user)):
    try:
        shared_info = await document_service.get_shared_users_for_document(document_id)
        if not shared_info:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found or not shared with any users")
        return shared_info
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.post("/documents/inicialize_compresion_job/{document_id}", response_model=dict)
async def inicialize_document_compresion_job(document_id: int, document_service: DocumentService = Depends(get_document_service)):
    try:
        job_info = await document_service.inicialize_document_compresion_job(document_id)
        return job_info
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.post("/documents/authenticated/inicialize_compresion_job/{document_id}", response_model=dict, tags=["Documents", "Authenticated"])
async def inicialize_document_compresion_job_authenticated(document_id: int, document_service: DocumentService = Depends(get_document_service), current_user: User = Depends(get_current_user)):
    try:
        job_info = await document_service.inicialize_document_compresion_job(document_id)
        return job_info
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# User Endpoints
@app.get("/users/", response_model=List[User])
async def list_all_users(offset: int = 0, limit: int = 100, user_service: UserService = Depends(get_user_service)):
    try:
        users = await user_service.list_users(offset, limit)
        print(f"Users: {users}")
        return users
    except Exception as e:
        print(f"Error listing users: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.get("/users/authenticated/", response_model=List[User], tags=["Users", "Authenticated"])
async def list_all_users_authenticated(offset: int = 0, limit: int = 100, user_service: UserService = Depends(get_user_service), current_user: User = Depends(get_current_user)):
    try:
        users = await user_service.list_users(offset, limit)
        return users
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.get("/users/{user_id}", response_model=User)
async def get_user_by_id(user_id: int, user_service: UserService = Depends(get_user_service)):
    try:
        user = await user_service.get_user(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user
    except Exception as e:
        raise e if e.status_code == status.HTTP_404_NOT_FOUND else  HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.get("/users/authenticated/{user_id}", response_model=User, tags=["Users", "Authenticated"])
async def get_user_by_id_authenticated(user_id: int, user_service: UserService = Depends(get_user_service), current_user: User = Depends(get_current_user)):
    try:
        user = await user_service.get_user(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.post("/users/", response_model=User)
async def create_new_user(user: UserCreate, user_service: UserService = Depends(get_user_service)):
    try:
        created_user = await user_service.create_user(user)
        return created_user
    except Exception as e:        
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.post("/users/authenticated/", response_model=User, tags=["Users", "Authenticated"])
async def create_new_user_authenticated(user: UserCreate, user_service: UserService = Depends(get_user_service), current_user: User = Depends(get_current_user)):
    try:
        created_user = await user_service.create_user(user)
        return created_user
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.put("/users/{user_id}", response_model=User)
async def update_existing_user(user_id: int, user: UserUpdate, user_service: UserService = Depends(get_user_service)):
    try:
        updated_user = await user_service.update_user(user_id, user)
        if not updated_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return updated_user
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.put("/users/authenticated/{user_id}", response_model=User, tags=["Users", "Authenticated"])
async def update_existing_user_authenticated(user_id: int, user: UserUpdate, user_service: UserService = Depends(get_user_service), current_user: User = Depends(get_current_user)):
    try:
        updated_user = await user_service.update_user(user_id, user)
        if not updated_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return updated_user
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.delete("/users/{user_id}", response_model=dict)
async def delete_existing_user(user_id: int, user_service: UserService = Depends(get_user_service)):
    try:
        result = await user_service.delete_user(user_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.delete("/users/authenticated/{user_id}", response_model=dict, tags=["Users", "Authenticated"])
async def delete_existing_user_authenticated(user_id: int, user_service: UserService = Depends(get_user_service), current_user: User = Depends(get_current_user)):
    try:
        result = await user_service.delete_user(user_id)
        print(f"Result: {result}")
        return result
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.get("/users/{user_id}/uploaded_documents", response_model=dict)
async def get_user_uploaded_documents(user_id: int, user_service: UserService = Depends(get_user_service)):
    try:
        user_documents = await user_service.get_documents_uploaded_by_user(user_id)
        if not user_documents:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found or no documents uploaded")
        return user_documents
    except Exception as e:
        raise e if e.status_code == status.HTTP_404_NOT_FOUND else  HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.get("/users/authenticated/{user_id}/uploaded_documents", response_model=dict, tags=["Users", "Authenticated"])
async def get_user_uploaded_documents_authenticated(user_id: int, user_service: UserService = Depends(get_user_service), current_user: User = Depends(get_current_user)):
    try:
        user_documents = await user_service.get_documents_uploaded_by_user(user_id)
        if not user_documents:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found or no documents uploaded")
        return user_documents
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.post("/users/{user_id}/assign_role/{role_id}", response_model=dict)
async def assign_role_to_user(user_id: int, role_id: int, user_service: UserService = Depends(get_user_service)):
    try:
        result = await user_service.assign_role_to_user(user_id, role_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.post("/users/authenticated/{user_id}/assign_role/{role_id}", response_model=dict, tags=["Users", "Authenticated"])
async def assign_role_to_user_authenticated(user_id: int, role_id: int, user_service: UserService = Depends(get_user_service), current_user: User = Depends(get_current_user)):
    try:
        result = await user_service.assign_role_to_user(user_id, role_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# Role Endpoints
@app.post("/roles/", response_model=Role)
async def create_new_role(role: RoleCreate, role_service: RoleService = Depends(get_role_service)):
    try:
        created_role = await role_service.create_role(role)
        return created_role
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.post("/roles/authenticated/", response_model=Role, tags=["Roles", "Authenticated"])
async def create_new_role_authenticated(role: RoleCreate, role_service: RoleService = Depends(get_role_service), current_user: User = Depends(get_current_user)):
    try:
        created_role = await role_service.create_role(role)
        return created_role
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.put("/roles/{role_id}", response_model=Role)
async def update_existing_role(role_id: int, role: RoleUpdate, role_service: RoleService = Depends(get_role_service)):
    try:
        updated_role = await role_service.update_role(role_id, role)
        if not updated_role:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
        return updated_role
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.put("/roles/authenticated/{role_id}", response_model=Role, tags=["Roles", "Authenticated"])
async def update_existing_role_authenticated(role_id: int, role: RoleUpdate, role_service: RoleService = Depends(get_role_service), current_user: User = Depends(get_current_user)):
    try:
        updated_role = await role_service.update_role(role_id, role)
        if not updated_role:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
        return updated_role
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.delete("/roles/{role_id}", response_model=dict)
async def delete_existing_role(role_id: int, role_service: RoleService = Depends(get_role_service)):
    try:
        result = await role_service.delete_role(role_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.delete("/roles/authenticated/{role_id}", response_model=dict, tags=["Roles", "Authenticated"])
async def delete_existing_role_authenticated(role_id: int, role_service: RoleService = Depends(get_role_service), current_user: User = Depends(get_current_user)):
    try:
        result = await role_service.delete_role(role_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.post("/roles/event", response_model=Log)
async def create_new_role_event(event: str, user_id: int, event_description: Optional[str] = None, role_service: RoleService = Depends(get_role_service)):
    try:
        log_entry = await role_service.create_role_event(event, user_id, event_description)
        return log_entry
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.post("/roles/authenticated/event", response_model=Log, tags=["Roles", "Authenticated"])
async def create_new_role_event_authenticated(event: str, user_id: int, event_description: Optional[str] = None, role_service: RoleService = Depends(get_role_service), current_user: User = Depends(get_current_user)):
    try:
        log_entry = await role_service.create_role_event(event, user_id, event_description)
        return log_entry
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# Log Endpoints
@app.post("/logs/", response_model=Log)
async def create_new_log(log_item: LogBase, log_service: LogService = Depends(get_log_service)):
    #event: str, user_id: Optional[int] = None, event_description: Optional[str] = None
    
    try:
        log_entry = await log_service.create_log(log_item.event, log_item.user_id, log_item.event_description)
        return log_entry
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.post("/logs/authenticated/", response_model=Log, tags=["Logs", "Authenticated"])
async def create_new_log_authenticated(log_item: LogBase, log_service: LogService = Depends(get_log_service), current_user: User = Depends(get_current_user)):
    try:
        log_entry = await log_service.create_log(log_item.event, log_item.user_id, log_item.event_description)
        return log_entry
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.get("/logs/", response_model=List[Log])
async def list_all_logs(offset: int = 0, limit: int = 100, log_service: LogService = Depends(get_log_service)):
    try:
        logs = await log_service.list_logs(offset, limit)
        return logs
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.get("/logs/authenticated/", response_model=List[Log], tags=["Logs", "Authenticated"])
async def list_all_logs_authenticated(offset: int = 0, limit: int = 100, log_service: LogService = Depends(get_log_service), current_user: User = Depends(get_current_user)):
    try:
        logs = await log_service.list_logs(offset, limit)
        return logs
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.get("/logs/{log_id}", response_model=Log)
async def get_log_by_id(log_id: int, log_service: LogService = Depends(get_log_service)):
    try:
        log_entry = await log_service.get_log(log_id)
        if not log_entry:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Log entry not found")
        return log_entry
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.get("/logs/authenticated/{log_id}", response_model=Log, tags=["Logs", "Authenticated"])
async def get_log_by_id_authenticated(log_id: int, log_service: LogService = Depends(get_log_service), current_user: User = Depends(get_current_user)):
    try:
        log_entry = await log_service.get_log(log_id)
        if not log_entry:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Log entry not found")
        return log_entry
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.get("/logs/user/{user_id}", response_model=List[Log])
async def get_logs_for_user(user_id: int, offset: int = 0, limit: int = 100, log_service: LogService = Depends(get_log_service)):
    try:
        logs = await log_service.get_logs_by_user(user_id, offset, limit)
        return logs
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.get("/logs/authenticated/user/{user_id}", response_model=List[Log], tags=["Logs", "Authenticated"])
async def get_logs_for_user_authenticated(user_id: int, offset: int = 0, limit: int = 100, log_service: LogService = Depends(get_log_service), current_user: User = Depends(get_current_user)):
    try:
        logs = await log_service.get_logs_by_user(user_id, offset, limit)
        return logs
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


##### Scheduler periodical task execution ########################




