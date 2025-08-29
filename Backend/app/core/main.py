from fastapi import FastAPI, Depends, HTTPException, status, UploadFile, APIRouter
from core.config import Settings
from db.base import get_db, SessionLocal, Base, engine
from db.seed import create_initial_data
from db.clean import clean_db_tables

from schemas.user import User, UserCreate, UserUpdate
from schemas.document import Document, DocumentCreate, DocumentUpdate
from schemas.role import Role, RoleCreate, RoleUpdate
from schemas.log import Log, LogCreate, LogUpdate
from schemas.document_shared import DocumentShared, DocumentSharedCreate, DocumentSharedUpdate
from schemas.user_role import UserRole, UserRoleCreate, UserRoleUpdate

from services.document_service import DocumentService
from services.user_service import UserService
from services.role_service import RoleService
from services.log_service import LogService
from typing import List, Optional
from sqlalchemy.orm import Session

settings = Settings()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
)

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        create_initial_data(db)
    finally:
        clean_db_tables(db)
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
    
###---  Main app services ------------------------------------------------------------

# Dependency to get DocumentService
async def get_document_service(db: Session = Depends(get_db)) -> DocumentService:
    return DocumentService(db)

# Dependency to get UserService
async def get_user_service(db: Session = Depends(get_db)) -> UserService:
    return UserService(db)

# Dependency to get RoleService
async def get_role_service(db: Session = Depends(get_db)) -> RoleService:
    return RoleService(db)

# Dependency to get LogService
async def get_log_service(db: Session = Depends(get_db)) -> LogService:
    return LogService(db)

# Document Endpoints
@app.post("/documents/upload_document/{document_id}", response_model=Document)
async def upload_document_info(document_id: int, document: DocumentCreate, document_service: DocumentService = Depends(get_document_service)):
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

@app.delete("/documents/{document_id}", response_model=dict)
async def delete_document(document_id: int, document_service: DocumentService = Depends(get_document_service)):
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

@app.get("/documents/", response_model=List[Document])
async def list_all_documents(document_service: DocumentService = Depends(get_document_service)):
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

@app.get("/documents/{document_id}/shared_by/users", response_model=List[User])
async def get_document_shared_users(document_id: int, document_service: DocumentService = Depends(get_document_service)):
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

# User Endpoints
@app.get("/users/", response_model=List[User])
async def list_all_users(offset: int = 0, limit: int = 100, user_service: UserService = Depends(get_user_service)):
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
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.post("/users/", response_model=User)
async def create_new_user(user: UserCreate, user_service: UserService = Depends(get_user_service)):
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

@app.delete("/users/{user_id}", response_model=dict)
async def delete_existing_user(user_id: int, user_service: UserService = Depends(get_user_service)):
    try:
        result = await user_service.delete_user(user_id)
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
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.post("/users/{user_id}/assign_role/{role_id}", response_model=dict)
async def assign_role_to_user(user_id: int, role_id: int, user_service: UserService = Depends(get_user_service)):
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

@app.put("/roles/{role_id}", response_model=Role)
async def update_existing_role(role_id: int, role: RoleUpdate, role_service: RoleService = Depends(get_role_service)):
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

@app.post("/roles/event", response_model=Log)
async def create_new_role_event(event: str, user_id: int, event_description: Optional[str] = None, role_service: RoleService = Depends(get_role_service)):
    try:
        log_entry = await role_service.create_role_event(event, user_id, event_description)
        return log_entry
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# Log Endpoints
@app.post("/logs/", response_model=Log)
async def create_new_log(event: str, user_id: Optional[int] = None, event_description: Optional[str] = None, log_service: LogService = Depends(get_log_service)):
    try:
        log_entry = await log_service.create_log(event, user_id, event_description)
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

@app.get("/logs/{log_id}", response_model=Log)
async def get_log_by_id(log_id: int, log_service: LogService = Depends(get_log_service)):
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

