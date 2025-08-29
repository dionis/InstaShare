import pytest
from models import Role, Log 
from schemas import RoleUpdate, RoleCreate
from unittest.mock import AsyncMock
from services.role_service import RoleService
from core.main import app


# All fixtures (client, mock_role_service) are in conftest.py

# Test Role Endpoints
@pytest.mark.asyncio
async def test_create_new_role(client, mock_role_service):
    role_create = {"role_name": "admin", "description": "Administrator role"}
    mock_role_service.create_role.return_value = Role(
        id=1, role_name="admin", description="Administrator role", updated_at="2024-01-01T00:00:00"
    )
    response = client.post("/roles/", json=role_create)
    assert response.status_code == 200
    assert response.json()["role_name"] == "admin"
    mock_role_service.create_role.assert_called_once()

@pytest.mark.asyncio
async def test_update_existing_role(client, mock_role_service):
    role_update = {"role_name": "super_admin"}
    mock_role_service.update_role.return_value = Role(
        id=1, role_name="super_admin", description="Administrator role", updated_at="2024-01-01T00:00:00"
    )
    response = client.put("/roles/1", json=role_update)
    assert response.status_code == 200
    assert response.json()["role_name"] == "super_admin"
    mock_role_service.update_role.assert_called_once_with(1, RoleUpdate(role_name="super_admin"))

@pytest.mark.asyncio
async def test_delete_existing_role(client, mock_role_service):
    mock_role_service.delete_role.return_value = {"action": "deleted", "message": "Role deleted"}
    response = client.delete("/roles/1")
    assert response.status_code == 200
    assert response.json()["action"] == "deleted"
    mock_role_service.delete_role.assert_called_once_with(1)

@pytest.mark.asyncio
async def test_create_new_role_event(client, mock_role_service):
    mock_role_service.create_role_event.return_value = Log(
        id=1, event="role_assigned", user_id=1, event_description="Role assigned to user", created_at="2024-01-01T00:00:00"
    )
    response = client.post("/roles/event?event=role_assigned&user_id=1&event_description=Role assigned to user")
    assert response.status_code == 200
    assert response.json()["event"] == "role_assigned"
    mock_role_service.create_role_event.assert_called_once_with("role_assigned", 1, "Role assigned to user")
