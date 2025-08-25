from fastapi.testclient import TestClient
import pytest
from unittest.mock import AsyncMock
from app.app.main import app, get_document_service, get_user_service, get_role_service, get_log_service
from app.app.services.document_service import DocumentService
from app.app.services.user_service import UserService
from app.app.services.role_service import RoleService
from app.app.services.log_service import LogService

client = TestClient(app)

@pytest.fixture
def mock_document_service():
    service = AsyncMock(spec=DocumentService)
    app.dependency_overrides[get_document_service] = lambda: service
    yield service
    app.dependency_overrides = {}

@pytest.fixture
def mock_user_service():
    service = AsyncMock(spec=UserService)
    app.dependency_overrides[get_user_service] = lambda: service
    yield service
    app.dependency_overrides = {}

@pytest.fixture
def mock_role_service():
    service = AsyncMock(spec=RoleService)
    app.dependency_overrides[get_role_service] = lambda: service
    yield service
    app.dependency_overrides = {}

@pytest.fixture
def mock_log_service():
    service = AsyncMock(spec=LogService)
    app.dependency_overrides[get_log_service] = lambda: service
    yield service
    app.dependency_overrides = {}
