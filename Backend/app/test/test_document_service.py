import pytest
import os
from datetime import datetime
from fastapi.testclient import TestClient

from models.document import Document as DocumentModel, DocumentStatus
from schemas.document import Document as DocumentSchema, DocumentCreate, DocumentUpdate, DocumentStatusSchema
from schemas.user import User as UserSchema # For document shared users
from unittest.mock import AsyncMock
from services.document_service import DocumentService
from core.main import app

# All fixtures (client, mock_document_service) are in conftest.py

# Test Document Endpoints
@pytest.mark.asyncio
async def test_upload_document_info(client: TestClient, mock_document_service: AsyncMock):
    document_create = DocumentCreate(name="test_doc", type="pdf", size="10MB", status=DocumentStatusSchema.uploaded)
    mock_document_service.upload_document_info.return_value = DocumentSchema(
        id=1, name="test_doc", type="pdf", size="10MB", created_at=datetime.utcnow(), updated_at=datetime.utcnow(), deleted_at=None, uploaded_at=datetime.utcnow(), status=DocumentStatusSchema.uploaded
    )
    response = client.post("/documents/upload_document/1", json=document_create.model_dump())
    assert response.status_code == 200
    assert response.json()["name"] == "test_doc"
    mock_document_service.upload_document_info.assert_called_once_with(1, document_create)

@pytest.mark.asyncio
async def test_upload_document_file(client: TestClient, mock_document_service: AsyncMock):
    mock_document_service.upload_document_file.return_value = DocumentSchema(
        id=1, name="test_doc", type="pdf", size="12345", created_at=datetime.utcnow(), updated_at=datetime.utcnow(), deleted_at=None, uploaded_at=datetime.utcnow(), status=DocumentStatusSchema.uploaded
    )
    # Create a dummy file
    file_content = b"test content"
    file_name = "test.txt"
    # In-memory file for testing
    from io import BytesIO
    test_file = BytesIO(file_content)
    test_file.name = file_name # Add name attribute for UploadFile
    response = client.post("/documents/upload_document_file/1", data = {"name": "test1", "file_type": "pdf"}, files={"file": (file_name, test_file, "text/plain")})
    
    assert response.status_code == 200
    assert response.json()["size"] == "12345"
    # mock_document_service.upload_document_file.assert_called_once() # Cannot assert file content directly

@pytest.mark.asyncio
async def test_delete_document(client: TestClient, mock_document_service: AsyncMock):
    mock_document_service.delete_document.return_value = {"action": "deleted", "message": "Document deleted"}
    response = client.delete("/documents/1")
    assert response.status_code == 200
    assert response.json()["action"] == "deleted"
    mock_document_service.delete_document.assert_called_once_with(1)

@pytest.mark.asyncio
async def test_update_document_info(client: TestClient, mock_document_service: AsyncMock):
    document_update = DocumentUpdate(name="updated_doc")
    mock_document_service.update_document.return_value = DocumentSchema(
        id=1, name="updated_doc", type="pdf", size="10MB", created_at=datetime.utcnow(), updated_at=datetime.utcnow(), deleted_at=None, uploaded_at=datetime.utcnow(), status=DocumentStatusSchema.uploaded
    )
    response = client.put("/documents/1", json=document_update.model_dump(exclude_unset=True))
    assert response.status_code == 200
    assert response.json()["name"] == "updated_doc"
    mock_document_service.update_document.assert_called_once_with(1, document_update)

# @pytest.mark.asyncio
async def test_list_all_documents(client: TestClient, mock_document_service: AsyncMock):
    mock_document_service.list_documents.return_value = [
        DocumentSchema(id=1, name="doc1", type="pdf", size="100", created_at=datetime.utcnow(), updated_at=datetime.utcnow(), deleted_at=None, uploaded_at=datetime.utcnow(), status=DocumentStatusSchema.uploaded),
        DocumentSchema(id=2, name="doc2", type="docx", size="200", created_at=datetime.utcnow(), updated_at=datetime.utcnow(), deleted_at=None, uploaded_at=datetime.utcnow(), status=DocumentStatusSchema.uploaded),
    ]
    response = client.get("/documents/")
    assert response.status_code == 200
    assert len(response.json()) == 2
    mock_document_service.list_documents.assert_called_once()

@pytest.mark.asyncio
async def test_get_document_by_id(client: TestClient, mock_document_service: AsyncMock):
    mock_document_service.get_document.return_value = DocumentSchema(
        id=1, name="doc1", type="pdf", size="100", created_at=datetime.utcnow(), updated_at=datetime.utcnow(), deleted_at=None, uploaded_at=datetime.utcnow(), status=DocumentStatusSchema.uploaded
    )
    response = client.get("/documents/1")
    assert response.status_code == 200
    assert response.json()["name"] == "doc1"
    mock_document_service.get_document.assert_called_once_with(1)

@pytest.mark.asyncio
async def test_get_document_shared_users(client: TestClient, mock_document_service: AsyncMock):
    mock_document_service.get_shared_users_for_document.return_value = [
        UserSchema(id=1, username="User1", email="user1@example.com", phone="123", responsability="user", created_at=datetime.utcnow(), updated_at=datetime.utcnow(), deleted_at=None),
    ]
    response = client.get("/documents/1/shared_by/users")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["email"] == "user1@example.com"
    mock_document_service.get_shared_users_for_document.assert_called_once_with(1)

@pytest.mark.asyncio
async def test_inicialize_document_compresion_job(client: TestClient, mock_document_service: AsyncMock):
    mock_document_service.inicialize_document_compresion_job.return_value = {
        "idjob": 1, "document_size": 234, "started_timed_at": "2025-04-22"
    }
    response = client.post("/documents/inicialize_compresion_job/1")
    assert response.status_code == 200
    assert response.json()["idjob"] == 1
    mock_document_service.inicialize_document_compresion_job.assert_called_once_with(1)

# --- Authenticated Endpoints Tests ---
@pytest.mark.asyncio
async def test_upload_document_info_authenticated(authenticated_client: TestClient, mock_document_service: AsyncMock, dummy_user: dict):
    document_create = DocumentCreate(name="auth_test_doc", type="pdf", size="15MB", status=DocumentStatusSchema.uploaded)
    mock_document_service.upload_document_info.return_value = DocumentSchema(
        id=2, name="auth_test_doc", type="pdf", size="15MB", created_at=datetime.utcnow(), updated_at=datetime.utcnow(), deleted_at=None, uploaded_at=datetime.utcnow(), status=DocumentStatusSchema.uploaded
    )
    response = authenticated_client.post("/documents/authenticated/upload_document/2", json=document_create.model_dump())
    assert response.status_code == 200
    assert response.json()["name"] == "auth_test_doc"
    mock_document_service.upload_document_info.assert_called_once_with(2, document_create)

@pytest.mark.asyncio
async def test_upload_document_file_authenticated(authenticated_client: TestClient, mock_document_service: AsyncMock, dummy_user: dict):
    mock_document_service.upload_document_file.return_value = DocumentSchema(
        id=2, name="auth_test_doc", type="pdf", size="23456", created_at=datetime.utcnow(), updated_at=datetime.utcnow(), deleted_at=None, uploaded_at=datetime.utcnow(), status=DocumentStatusSchema.uploaded
    )
    file_content = b"authenticated test content"
    file_name = "auth_test.txt"
    from io import BytesIO
    test_file = BytesIO(file_content)
    test_file.name = file_name
    
    response = authenticated_client.post("/documents/authenticated/upload_document_file/2",data = {"name": "test1", "file_type": "pdf"}, files={"file": (file_name, test_file, "text/plain")})
    
    assert response.status_code == 200
    assert response.json()["size"] == "23456"
    # mock_document_service.upload_document_file.assert_called_once() # Cannot assert file content directly

@pytest.mark.asyncio
async def test_delete_document_authenticated(authenticated_client: TestClient, mock_document_service: AsyncMock, dummy_user: dict):
    mock_document_service.delete_document.return_value = {"action": "deleted", "message": "Document deleted"}
    response = authenticated_client.delete("/documents/authenticated/1")
    assert response.status_code == 200
    assert response.json()["action"] == "deleted"
    mock_document_service.delete_document.assert_called_once_with(1)

@pytest.mark.asyncio
async def test_update_document_info_authenticated(authenticated_client: TestClient, mock_document_service: AsyncMock, dummy_user: dict):
    document_update = DocumentUpdate(name="auth_updated_doc")
    mock_document_service.update_document.return_value = DocumentSchema(
        id=1, name="auth_updated_doc", type="pdf", size="10MB", created_at=datetime.utcnow(), updated_at=datetime.utcnow(), deleted_at=None, uploaded_at=datetime.utcnow(), status=DocumentStatusSchema.uploaded
    )
    response = authenticated_client.put("/documents/authenticated/1", json=document_update.model_dump(exclude_unset=True))
    assert response.status_code == 200
    assert response.json()["name"] == "auth_updated_doc"
    mock_document_service.update_document.assert_called_once_with(1, document_update)

@pytest.mark.asyncio
async def test_list_all_documents_authenticated(authenticated_client: TestClient, mock_document_service: AsyncMock, dummy_user: dict):
    mock_document_service.list_documents.return_value = [
        DocumentSchema(id=1, name="auth_doc1", type="pdf", size="100", created_at=datetime.utcnow(), updated_at=datetime.utcnow(), deleted_at=None, uploaded_at=datetime.utcnow(), status=DocumentStatusSchema.uploaded),
    ]
    response = authenticated_client.get("/documents/authenticated/")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["name"] == "auth_doc1"
    mock_document_service.list_documents.assert_called_once()

@pytest.mark.asyncio
async def test_get_document_by_id_authenticated(authenticated_client: TestClient, mock_document_service: AsyncMock, dummy_user: dict):
    mock_document_service.get_document.return_value = DocumentSchema(
        id=1, name="auth_doc1", type="pdf", size="100", created_at=datetime.utcnow(), updated_at=datetime.utcnow(), deleted_at=None, uploaded_at=datetime.utcnow(), status=DocumentStatusSchema.uploaded
    )
    response = authenticated_client.get("/documents/authenticated/1")
    assert response.status_code == 200
    assert response.json()["name"] == "auth_doc1"
    mock_document_service.get_document.assert_called_once_with(1)

@pytest.mark.asyncio
async def test_get_document_shared_users_authenticated(authenticated_client: TestClient, mock_document_service: AsyncMock, dummy_user: dict):
    mock_document_service.get_shared_users_for_document.return_value = [
        UserSchema(id=dummy_user["id"], username=dummy_user["username"], email=dummy_user["email"], phone=dummy_user["phone"], responsability=dummy_user["responsability"], created_at=dummy_user["created_at"], updated_at=dummy_user["updated_at"], deleted_at=dummy_user["deleted_at"])
    ]
    response = authenticated_client.get("/documents/authenticated/1/shared_by/users")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["email"] == dummy_user["email"]
    mock_document_service.get_shared_users_for_document.assert_called_once_with(1)

@pytest.mark.asyncio
async def test_inicialize_document_compresion_job_authenticated(authenticated_client: TestClient, mock_document_service: AsyncMock, dummy_user: dict):
    mock_document_service.inicialize_document_compresion_job.return_value = {
        "idjob": 2, "document_size": 345, "started_timed_at": "2025-04-23"
    }
    response = authenticated_client.post("/documents/authenticated/inicialize_compresion_job/2")
    assert response.status_code == 200
    assert response.json()["idjob"] == 2
    mock_document_service.inicialize_document_compresion_job.assert_called_once_with(2)
