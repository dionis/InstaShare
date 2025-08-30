import pytest
from datetime import datetime
from fastapi.testclient import TestClient

from ..models.role import Role as RoleModel
from ..models.log import Log as LogModel
from ..schemas.role import Role as RoleSchema, RoleCreate, RoleUpdate
from ..schemas.log import Log as LogSchema
from ..schemas.user import User as UserSchema # For authenticated client fixture
from unittest.mock import AsyncMock
from ..services.role_service import RoleService
from ..core.main import app


# All fixtures (client, mock_role_service, authenticated_client, dummy_user) are in conftest.py

# Test Role Endpoints
@pytest.mark.asyncio
async def test_create_new_role(client: TestClient, mock_role_service: AsyncMock):
    role_create_data = RoleCreate(role_name="admin", description="Administrator role")
    mock_role_service.create_role.return_value = RoleSchema(
        id=1, created_at=datetime.utcnow(), updated_at=datetime.utcnow(), deleted_at=None, **role_create_data.model_dump()
    )
    response = client.post("/roles/", json=role_create_data.model_dump())
    assert response.status_code == 200
    assert response.json()["role_name"] == "admin"
    mock_role_service.create_role.assert_called_once_with(role_create_data)

@pytest.mark.asyncio
async def test_update_existing_role(client: TestClient, mock_role_service: AsyncMock):
    role_update_data = RoleUpdate(role_name="super_admin")
    mock_role_service.update_role.return_value = RoleSchema(
        id=1, role_name="super_admin", description="Administrator role", created_at=datetime.utcnow(), updated_at=datetime.utcnow(), deleted_at=None
    )
    response = client.put("/roles/1", json=role_update_data.model_dump(exclude_unset=True))
    assert response.status_code == 200
    assert response.json()["role_name"] == "super_admin"
    mock_role_service.update_role.assert_called_once_with(1, role_update_data)

@pytest.mark.asyncio
async def test_delete_existing_role(client: TestClient, mock_role_service: AsyncMock):
    mock_role_service.delete_role.return_value = {"action": "deleted", "message": "Role deleted"}
    response = client.delete("/roles/1")
    assert response.status_code == 200
    assert response.json()["action"] == "deleted"
    mock_role_service.delete_role.assert_called_once_with(1)

@pytest.mark.asyncio
async def test_create_new_role_event(client: TestClient, mock_role_service: AsyncMock):
    mock_role_service.create_role_event.return_value = LogSchema(
        id=1, event="role_assigned", user_id=1, event_description="Role assigned to user", created_at=datetime.utcnow(), updated_at=datetime.utcnow(), deleted_at=None
    )
    response = client.post("/roles/event?event=role_assigned&user_id=1&event_description=Role assigned to user")
    assert response.status_code == 200
    assert response.json()["event"] == "role_assigned"
    mock_role_service.create_role_event.assert_called_once_with("role_assigned", 1, "Role assigned to user")

# --- Authenticated Endpoints Tests ---
@pytest.mark.asyncio
async def test_create_new_role_authenticated(authenticated_client: TestClient, mock_role_service: AsyncMock, dummy_user: dict):
    role_create_data = RoleCreate(role_name="auth_editor", description="Authenticated Editor role")
    mock_role_service.create_role.return_value = RoleSchema(
        id=2, created_at=datetime.utcnow(), updated_at=datetime.utcnow(), deleted_at=None, **role_create_data.model_dump()
    )
    response = authenticated_client.post("/roles/authenticated/", json=role_create_data.model_dump())
    assert response.status_code == 200
    assert response.json()["role_name"] == "auth_editor"
    mock_role_service.create_role.assert_called_once_with(role_create_data)

@pytest.mark.asyncio
async def test_update_existing_role_authenticated(authenticated_client: TestClient, mock_role_service: AsyncMock, dummy_user: dict):
    role_update_data = RoleUpdate(role_name="auth_super_editor")
    mock_role_service.update_role.return_value = RoleSchema(
        id=1, role_name="auth_super_editor", description="Administrator role", created_at=datetime.utcnow(), updated_at=datetime.utcnow(), deleted_at=None
    )
    response = authenticated_client.put("/roles/authenticated/1", json=role_update_data.model_dump(exclude_unset=True))
    assert response.status_code == 200
    assert response.json()["role_name"] == "auth_super_editor"
    mock_role_service.update_role.assert_called_once_with(1, role_update_data)

@pytest.mark.asyncio
async def test_delete_existing_role_authenticated(authenticated_client: TestClient, mock_role_service: AsyncMock, dummy_user: dict):
    mock_role_service.delete_role.return_value = {"action": "deleted", "message": "Role deleted"}
    response = authenticated_client.delete("/roles/authenticated/1")
    assert response.status_code == 200
    assert response.json()["action"] == "deleted"
    mock_role_service.delete_role.assert_called_once_with(1)

@pytest.mark.asyncio
async def test_create_new_role_event_authenticated(authenticated_client: TestClient, mock_role_service: AsyncMock, dummy_user: dict):
    mock_role_service.create_role_event.return_value = LogSchema(
        id=2, event="auth_role_assigned", user_id=dummy_user["id"], event_description="Authenticated Role assigned", created_at=datetime.utcnow(), updated_at=datetime.utcnow(), deleted_at=None
    )
    response = authenticated_client.post(f"/roles/authenticated/event?event=auth_role_assigned&user_id={dummy_user["id"]}&event_description=Authenticated Role assigned")
    assert response.status_code == 200
    assert response.json()["event"] == "auth_role_assigned"
    mock_role_service.create_role_event.assert_called_once_with("auth_role_assigned", dummy_user["id"], "Authenticated Role assigned")
