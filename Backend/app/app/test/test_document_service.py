import pytest
import os
from app.app.models.models import Document, DocumentCreate, DocumentUpdate

# All fixtures (client, mock_document_service) are in conftest.py

# Test Document Endpoints
@pytest.mark.asyncio
async def test_upload_document_info(client, mock_document_service):
    document_create = DocumentCreate(name="test_doc", type="pdf", uploaded_by_user_id=1, file_path="path/to/file")
    mock_document_service.upload_document_info.return_value = Document(
        id=1, name="test_doc", type="pdf", size=0, uploaded_at="2024-01-01T00:00:00", status="uploaded", uploaded_by_user_id=1, file_path="path/to/file"
    )
    response = client.post("/documents/upload_document/1", json=document_create.model_dump())
    assert response.status_code == 200
    assert response.json()["name"] == "test_doc"
    mock_document_service.upload_document_info.assert_called_once()

@pytest.mark.asyncio
async def test_upload_document_file(client, mock_document_service):
    mock_document_service.upload_document_file.return_value = Document(
        id=1, name="test_doc", type="pdf", size=12345, uploaded_at="2024-01-01T00:00:00", status="uploaded", uploaded_by_user_id=1, file_path="path/to/file"
    )
    with open("test.txt", "w") as f:
        f.write("test content")
    with open("test.txt", "rb") as f:
        response = client.post("/documents/upload_document_file/1", files={"file": ("test.txt", f, "text/plain")})
    os.remove("test.txt")
    assert response.status_code == 200
    assert response.json()["size"] == 12345
    mock_document_service.upload_document_file.assert_called_once()

@pytest.mark.asyncio
async def test_delete_document(client, mock_document_service):
    mock_document_service.delete_document.return_value = {"action": "deleted", "message": "Document deleted"}
    response = client.delete("/documents/1")
    assert response.status_code == 200
    assert response.json()["action"] == "deleted"
    mock_document_service.delete_document.assert_called_once_with(1)

@pytest.mark.asyncio
async def test_update_document_info(client, mock_document_service):
    document_update = DocumentUpdate(name="updated_doc")
    mock_document_service.update_document_info.return_value = Document(
        id=1, name="updated_doc", type="pdf", size=0, uploaded_at="2024-01-01T00:00:00", status="uploaded", uploaded_by_user_id=1, file_path="path/to/file"
    )
    response = client.put("/documents/1", json=document_update.model_dump())
    assert response.status_code == 200
    assert response.json()["name"] == "updated_doc"
    mock_document_service.update_document_info.assert_called_once()

@pytest.mark.asyncio
async def test_list_all_documents(client, mock_document_service):
    mock_document_service.list_documents.return_value = [
        Document(id=1, name="doc1", type="pdf", size=100, uploaded_at="2024-01-01T00:00:00", status="uploaded", uploaded_by_user_id=1, file_path="path/to/file"),
        Document(id=2, name="doc2", type="docx", size=200, uploaded_at="2024-01-01T00:00:00", status="uploaded", uploaded_by_user_id=1, file_path="path/to/file"),
    ]
    response = client.get("/documents/")
    assert response.status_code == 200
    assert len(response.json()) == 2
    mock_document_service.list_documents.assert_called_once()

@pytest.mark.asyncio
async def test_get_document_by_id(client, mock_document_service):
    mock_document_service.get_document.return_value = Document(
        id=1, name="doc1", type="pdf", size=100, uploaded_at="2024-01-01T00:00:00", status="uploaded", uploaded_by_user_id=1, file_path="path/to/file"
    )
    response = client.get("/documents/1")
    assert response.status_code == 200
    assert response.json()["name"] == "doc1"
    mock_document_service.get_document.assert_called_once_with(1)

@pytest.mark.asyncio
async def test_get_document_shared_users(client, mock_document_service):
    mock_document_service.get_shared_users_for_document.return_value = {
        "id": 1,
        "name": "doc1",
        "type": "pdf",
        "size": 100,
        "uploaded_at": "2024-01-01T00:00:00",
        "shared_with": [
            {"id": 1, "name": "User1", "email": "user1@example.com", "phone": "123", "shared_date": "2024-01-01"},
        ],
    }
    response = client.get("/documents/1/shared_by/users")
    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert len(response.json()["shared_with"]) == 1
    mock_document_service.get_shared_users_for_document.assert_called_once_with(1)

@pytest.mark.asyncio
async def test_inicialize_document_compresion_job(client, mock_document_service):
    mock_document_service.inicialize_document_compresion_job.return_value = {
        "idjob": 1, "document_size": 234, "started_timed_at": "2025-04-22"
    }
    response = client.post("/documents/inicialize_compresion_job/1")
    assert response.status_code == 200
    assert response.json()["idjob"] == 1
    mock_document_service.inicialize_document_compresion_job.assert_called_once_with(1)
