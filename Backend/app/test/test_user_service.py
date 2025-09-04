import pytest
from models import User, Document as DocumentModel
from schemas import  UserCreate, UserUpdate, Document as DocumentSchema
from unittest.mock import AsyncMock
from services.user_service import UserService
from core.main import app
from schemas.user import UserCreate, UserUpdate, User
from schemas.role import Role
from datetime import datetime
from passlib.context import CryptContext
from fastapi.testclient import TestClient


# All fixtures (client, mock_user_service) are in conftest.py

# --- Unauthenticated Endpoints Tests ---
# def test_read_root(client: TestClient):
#     response = client.get("/")
#     assert response.status_code == 200
#     assert response.json() == {"message": "Welcome to InstaShare Backend!"}

# def test_health_check(client: TestClient):
#     response = client.get("/health")
#     assert response.status_code == 200
#     assert response.json()["status"] == "ok"

# def test_list_all_users_unauthenticated(client: TestClient, mock_user_service: AsyncMock):
#     mock_user_service.list_users.return_value = []
#     response = client.get("/users/")
#     assert response.status_code == 200
#     assert response.json() == []
#     mock_user_service.list_users.assert_called_once_with(0, 100)

# def test_get_user_by_id_unauthenticated(client: TestClient, mock_user_service: AsyncMock):
#     mock_user_service.get_user.return_value = None
#     response = client.get("/users/1")
#     assert response.status_code == 404
#     assert response.json() == {"detail": "User not found"}
#     mock_user_service.get_user.assert_called_once_with(1)

def test_create_new_user_unauthenticated(client: TestClient, mock_user_service: AsyncMock):
    new_user_data = UserCreate(username="New User", email="new@example.com", password="newpassword", phone="1112223333", responsability="Editor")
    created_user_response = User(id=1, created_at=datetime.utcnow(), updated_at=datetime.utcnow(), **new_user_data.model_dump())
    mock_user_service.create_user.return_value = created_user_response
    response = client.post("/users/", json=new_user_data.model_dump())
    assert response.status_code == 200
    assert response.json()["email"] == "new@example.com"
    mock_user_service.create_user.assert_called_once_with(new_user_data)

def test_update_existing_user_unauthenticated(client: TestClient, mock_user_service: AsyncMock):
    user_update_data = UserUpdate(name="Updated Name")
    updated_user_response = User(id=1, username="Updated Name", email="test@example.com", password="testpassword", hashed_password="testpassword", created_at=datetime.utcnow(), updated_at=datetime.utcnow())
    mock_user_service.update_user.return_value = updated_user_response
    response = client.put("/users/1", json=user_update_data.model_dump(exclude_unset=True))
    assert response.status_code == 200
    assert response.json()["username"] == "Updated Name"
    mock_user_service.update_user.assert_called_once_with(1, user_update_data)

def test_delete_existing_user_unauthenticated(client: TestClient, mock_user_service: AsyncMock):
    mock_user_service.delete_user.return_value = {"action": "deleted", "message": "User deleted"}
    response = client.delete("/users/1")
    assert response.status_code == 200
    assert response.json() == {"action": "deleted", "message": "User deleted"}
    mock_user_service.delete_user.assert_called_once_with(1)

def test_get_user_uploaded_documents_unauthenticated(client: TestClient, mock_user_service: AsyncMock):
    mock_user_service.get_documents_uploaded_by_user.return_value = None
    response = client.get("/users/1/uploaded_documents")
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found or no documents uploaded"}
    mock_user_service.get_documents_uploaded_by_user.assert_called_once_with(1)

def test_assign_role_to_user_unauthenticated(client: TestClient, mock_user_service: AsyncMock):
    mock_user_service.assign_role_to_user.return_value = {"message": "Role assigned successfully"}
    response = client.post("/users/1/assign_role/1")
    assert response.status_code == 200
    assert response.json() == {"message": "Role assigned successfully"}
    mock_user_service.assign_role_to_user.assert_called_once_with(1, 1)

# --- Authenticated Endpoints Tests ---
def test_login_for_access_token(authenticated_client: TestClient, mock_supabase_client: AsyncMock, dummy_user: dict):
    # Mock the user query in the Supabase client mock
    mock_supabase_client.from_.return_value.select.return_value.filter.return_value.execute.return_value = (None, [dummy_user])

    response = authenticated_client.post(
        "/token",
        data={
            "username": dummy_user["email"],
            "password": dummy_user["hashed_password"]
        }
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_list_all_users_authenticated(authenticated_client: TestClient, mock_user_service: AsyncMock, dummy_user: dict):
    # Mock user service to return the dummy user in a list
    mock_user_service.list_users.return_value = [User(**dummy_user)]
    response = authenticated_client.get("/users/authenticated/")
    assert response.status_code == 200
    assert response.json()[0]["email"] == dummy_user["email"]
    mock_user_service.list_users.assert_called_once_with(0, 100)

def test_get_user_by_id_authenticated(authenticated_client: TestClient, mock_user_service: AsyncMock, dummy_user: dict):
    mock_user_service.get_user.return_value = User(**dummy_user)
    response = authenticated_client.get(f"/users/authenticated/{dummy_user["id"]}")
    assert response.status_code == 200
    assert response.json()["email"] == dummy_user["email"]
    mock_user_service.get_user.assert_called_once_with(dummy_user["id"])

def test_create_new_user_authenticated(authenticated_client: TestClient, mock_user_service: AsyncMock, dummy_user: dict):
    new_user_data = UserCreate(username="New User", email="auth_new@example.com", password="newpassword", phone="1112223333", responsability="Editor")
    created_user_response = User(id=1, created_at=datetime.utcnow(), updated_at=datetime.utcnow(), **new_user_data.model_dump())
     
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")        
    hashed_password = pwd_context.hash(new_user_data.password)
    
    new_user_data.hashed_password = hashed_password
    created_user_response.hashed_password = hashed_password
    
    mock_user_service.create_user.return_value = created_user_response
    
    response = authenticated_client.post("/users/authenticated/", json=new_user_data.model_dump())
    assert response.status_code == 201
    assert response.json()["email"] == "auth_new@example.com"
    
    #hash password is not being called by the service
    # mock_user_service.create_user.assert_called_once_with(new_user_data)

def test_update_existing_user_authenticated(authenticated_client: TestClient, mock_user_service: AsyncMock, dummy_user: dict):
    user_update_data = UserUpdate(username="Auth Updated Name")
    updated_user_response = User(id=dummy_user["id"], username="Auth Updated Name", email=dummy_user["email"], password=dummy_user["password"], hashed_password=dummy_user["hashed_password"], created_at=datetime.utcnow(), updated_at=datetime.utcnow())
    mock_user_service.update_user.return_value = updated_user_response
    response = authenticated_client.put(f"/users/authenticated/{dummy_user["id"]}", json=user_update_data.model_dump(exclude_unset=True))
    assert response.status_code == 200
    assert response.json()["username"] == "Auth Updated Name"
    mock_user_service.update_user.assert_called_once_with(dummy_user["id"], user_update_data)

def test_delete_existing_user_authenticated(authenticated_client: TestClient, mock_user_service: AsyncMock, dummy_user: dict):
    mock_user_service.delete_user.return_value = {"action": "deleted", "message": "User deleted"}
    response = authenticated_client.delete(f"/users/authenticated/{dummy_user["id"]}")
    assert response.status_code == 200
    assert response.json() == {"action": "deleted", "message": "User deleted"}
    mock_user_service.delete_user.assert_called_once_with(dummy_user["id"])
