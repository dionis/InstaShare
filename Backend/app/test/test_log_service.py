import pytest
from datetime import datetime
from fastapi.testclient import TestClient

from ..models.log import Log as LogModel
from ..schemas.log import Log as LogSchema, LogCreate, LogUpdate
from unittest.mock import AsyncMock
from ..services.log_service import LogService
from ..core.main import app

# All fixtures (client, mock_log_service) are in conftest.py

# Test Log Endpoints
@pytest.mark.asyncio
async def test_create_new_log(client: TestClient, mock_log_service: AsyncMock):
    log_create = LogCreate(event="user_login", user_id=1, event_description="User logged in")
    mock_log_service.create_log.return_value = LogSchema(
        id=1, created_at=datetime.utcnow(), updated_at=datetime.utcnow(), deleted_at=None, **log_create.model_dump()
    )
    response = client.post("/logs/", json=log_create.model_dump())
    assert response.status_code == 200
    assert response.json()["event"] == "user_login"
    mock_log_service.create_log.assert_called_once_with(log_create.event, log_create.user_id, log_create.event_description)

@pytest.mark.asyncio
async def test_list_all_logs(client: TestClient, mock_log_service: AsyncMock):
    mock_log_service.list_logs.return_value = [
        LogSchema(id=1, event="user_login", user_id=1, event_description="User logged in", created_at=datetime.utcnow(), updated_at=datetime.utcnow(), deleted_at=None),
        LogSchema(id=2, event="document_upload", user_id=1, event_description="Document uploaded", created_at=datetime.utcnow(), updated_at=datetime.utcnow(), deleted_at=None),
    ]
    response = client.get("/logs/")
    assert response.status_code == 200
    assert len(response.json()) == 2
    mock_log_service.list_logs.assert_called_once_with(0, 100)

@pytest.mark.asyncio
async def test_get_log_by_id(client: TestClient, mock_log_service: AsyncMock):
    mock_log_service.get_log.return_value = LogSchema(
        id=1, event="user_login", user_id=1, event_description="User logged in", created_at=datetime.utcnow(), updated_at=datetime.utcnow(), deleted_at=None
    )
    response = client.get("/logs/1")
    assert response.status_code == 200
    assert response.json()["event"] == "user_login"
    mock_log_service.get_log.assert_called_once_with(1)

@pytest.mark.asyncio
async def test_get_logs_for_user(client: TestClient, mock_log_service: AsyncMock):
    mock_log_service.get_logs_by_user.return_value = [
        LogSchema(id=1, event="user_login", user_id=1, event_description="User logged in", created_at=datetime.utcnow(), updated_at=datetime.utcnow(), deleted_at=None),
    ]
    response = client.get("/logs/user/1")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["user_id"] == 1
    mock_log_service.get_logs_by_user.assert_called_once_with(1, 0, 100)

# --- Authenticated Endpoints Tests ---
@pytest.mark.asyncio
async def test_create_new_log_authenticated(authenticated_client: TestClient, mock_log_service: AsyncMock, dummy_user: dict):
    log_create = LogCreate(event="auth_user_action", user_id=dummy_user["id"], event_description="Authenticated user action")
    mock_log_service.create_log.return_value = LogSchema(
        id=3, created_at=datetime.utcnow(), updated_at=datetime.utcnow(), deleted_at=None, **log_create.model_dump()
    )
    response = authenticated_client.post("/logs/authenticated/", json=log_create.model_dump())
    assert response.status_code == 200
    assert response.json()["event"] == "auth_user_action"
    mock_log_service.create_log.assert_called_once_with(log_create.event, log_create.user_id, log_create.event_description)

@pytest.mark.asyncio
async def test_list_all_logs_authenticated(authenticated_client: TestClient, mock_log_service: AsyncMock, dummy_user: dict):
    mock_log_service.list_logs.return_value = [
        LogSchema(id=3, event="auth_user_login", user_id=dummy_user["id"], event_description="Auth User logged in", created_at=datetime.utcnow(), updated_at=datetime.utcnow(), deleted_at=None),
    ]
    response = authenticated_client.get("/logs/authenticated/")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["event"] == "auth_user_login"
    mock_log_service.list_logs.assert_called_once_with(0, 100)

@pytest.mark.asyncio
async def test_get_log_by_id_authenticated(authenticated_client: TestClient, mock_log_service: AsyncMock, dummy_user: dict):
    mock_log_service.get_log.return_value = LogSchema(
        id=3, event="auth_user_login", user_id=dummy_user["id"], event_description="Auth User logged in", created_at=datetime.utcnow(), updated_at=datetime.utcnow(), deleted_at=None
    )
    response = authenticated_client.get(f"/logs/authenticated/{3}")
    assert response.status_code == 200
    assert response.json()["event"] == "auth_user_login"
    mock_log_service.get_log.assert_called_once_with(3)

@pytest.mark.asyncio
async def test_get_logs_for_user_authenticated(authenticated_client: TestClient, mock_log_service: AsyncMock, dummy_user: dict):
    mock_log_service.get_logs_by_user.return_value = [
        LogSchema(id=3, event="auth_user_login", user_id=dummy_user["id"], event_description="Auth User logged in", created_at=datetime.utcnow(), updated_at=datetime.utcnow(), deleted_at=None),
    ]
    response = authenticated_client.get(f"/logs/authenticated/user/{dummy_user["id"]}")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["user_id"] == dummy_user["id"]
    mock_log_service.get_logs_by_user.assert_called_once_with(dummy_user["id"], 0, 100)
