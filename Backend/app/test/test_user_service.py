import pytest
from models import User, Document as DocumentModel
from schemas import  UserCreate, UserUpdate, Document as DocumentSchema
from unittest.mock import AsyncMock
from services.user_service import UserService
from core.main import app



# All fixtures (client, mock_user_service) are in conftest.py

# Test User Endpoints
@pytest.mark.asyncio
async def test_list_all_users(client, mock_user_service):
    mock_user_service.list_users.return_value = [
        User(id=1, name="User1", email="user1@example.com", password="hashed_password", phone="123", responsability="Dev", created_at="2024-01-01T00:00:00", updated_at="2024-01-01T00:00:00"),
        User(id=2, name="User2", email="user2@example.com", password="hashed_password", phone="456", responsability="QA", created_at="2024-01-01T00:00:00", updated_at="2024-01-01T00:00:00"),
    ]
    response = client.get("/users")
    assert response.status_code == 200
    assert len(response.json()) == 2
    mock_user_service.list_users.assert_called_once_with(0, 100)

@pytest.mark.asyncio
async def test_get_user_by_id(client, mock_user_service):
    mock_user_service.get_user.return_value = User(
        id=1, name="User1", email="user1@example.com", password="hashed_password", phone="123", responsability="Dev", created_at="2024-01-01T00:00:00", updated_at="2024-01-01T00:00:00"
    )
    response = client.get("/users/1")
    assert response.status_code == 200
    assert response.json()["name"] == "User1"
    mock_user_service.get_user.assert_called_once_with(1)

@pytest.mark.asyncio
async def test_create_new_user(client, mock_user_service):
    user_create = UserCreate(name="NewUser", email="newuser@example.com", password="new_password", phone="789", responsability="Dev")
    mock_user_service.create_user.return_value = User(
        id=3, name="NewUser", email="newuser@example.com", password="hashed_new_password", phone="789", responsability="Dev", created_at="2024-01-01T00:00:00", updated_at="2024-01-01T00:00:00"
    )
    response = client.post("/users/", json=user_create.model_dump())
    assert response.status_code == 200
    assert response.json()["name"] == "NewUser"
    mock_user_service.create_user.assert_called_once()

@pytest.mark.asyncio
async def test_update_existing_user(client, mock_user_service):
    user_update = UserUpdate(name="UpdatedUser")
    mock_user_service.update_user.return_value = User(
        id=1, name="UpdatedUser", email="user1@example.com", password="hashed_password", phone="123", responsability="Dev", created_at="2024-01-01T00:00:00", updated_at="2024-01-01T00:00:00"
    )
    response = client.put("/users/1", json=user_update.model_dump())
    assert response.status_code == 200
    assert response.json()["name"] == "UpdatedUser"
    mock_user_service.update_user.assert_called_once()

@pytest.mark.asyncio
async def test_delete_existing_user(client, mock_user_service):
    mock_user_service.delete_user.return_value = {"action": "deleted", "message": "User deleted"}
    response = client.delete("/users/1")
    assert response.status_code == 200
    assert response.json()["action"] == "deleted"
    mock_user_service.delete_user.assert_called_once_with(1)

@pytest.mark.asyncio
async def test_get_user_uploaded_documents(client, mock_user_service):
    mock_user_service.get_documents_uploaded_by_user.return_value = {
        "id": 1,
        "name": "User1",
        "email": "user1@example.com",
        "uploaded_documents": [
            {"id": 1, "name": "doc1", "type": "pdf", "size": 100, "uploaded_at": "2024-01-01T00:00:00"},
        ],
    }
    response = client.get("/users/1/uploaded_documents")
    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert len(response.json()["uploaded_documents"]) == 1
    mock_user_service.get_documents_uploaded_by_user.assert_called_once_with(1)

@pytest.mark.asyncio
async def test_assign_role_to_user(client, mock_user_service):
    mock_user_service.assign_role_to_user.return_value = {"user_id": 1, "role_id": 1, "status": "assigned"}
    response = client.post("/users/1/assign_role/1")
    assert response.status_code == 200
    assert response.json()["status"] == "assigned"
    mock_user_service.assign_role_to_user.assert_called_once_with(1, 1)
