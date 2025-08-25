import pytest
from app.app.models.models import Log

# All fixtures (client, mock_log_service) are in conftest.py

# Test Log Endpoints
@pytest.mark.asyncio
async def test_create_new_log(client, mock_log_service):
    mock_log_service.create_log.return_value = Log(
        id=1, event="user_login", user_id=1, event_description="User logged in", created_at="2024-01-01T00:00:00"
    )
    response = client.post("/logs/?event=user_login&user_id=1&event_description=User logged in")
    assert response.status_code == 200
    assert response.json()["event"] == "user_login"
    mock_log_service.create_log.assert_called_once_with("user_login", 1, "User logged in")

@pytest.mark.asyncio
async def test_list_all_logs(client, mock_log_service):
    mock_log_service.list_logs.return_value = [
        Log(id=1, event="user_login", user_id=1, event_description="User logged in", created_at="2024-01-01T00:00:00"),
        Log(id=2, event="document_upload", user_id=1, event_description="Document uploaded", created_at="2024-01-01T00:00:00"),
    ]
    response = client.get("/logs/")
    assert response.status_code == 200
    assert len(response.json()) == 2
    mock_log_service.list_logs.assert_called_once_with(0, 100)

@pytest.mark.asyncio
async def test_get_log_by_id(client, mock_log_service):
    mock_log_service.get_log.return_value = Log(
        id=1, event="user_login", user_id=1, event_description="User logged in", created_at="2024-01-01T00:00:00"
    )
    response = client.get("/logs/1")
    assert response.status_code == 200
    assert response.json()["event"] == "user_login"
    mock_log_service.get_log.assert_called_once_with(1)

@pytest.mark.asyncio
async def test_get_logs_for_user(client, mock_log_service):
    mock_log_service.get_logs_by_user.return_value = [
        Log(id=1, event="user_login", user_id=1, event_description="User logged in", created_at="2024-01-01T00:00:00"),
    ]
    response = client.get("/logs/user/1")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["user_id"] == 1
    mock_log_service.get_logs_by_user.assert_called_once_with(1, 0, 100)
