import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from core.main import app
from db.base import Base, get_db

from unittest.mock import AsyncMock
from core.main import app, get_document_service, get_user_service, get_role_service, get_log_service
from services.document_service import DocumentService
from services.user_service import UserService
from services.role_service import RoleService
from services.log_service import LogService

# Use an in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
SessionTesting = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(name="session")
def session_fixture():
    Base.metadata.create_all(engine)  # Create tables
    with SessionTesting() as session:
        yield session
    Base.metadata.drop_all(engine)  # Drop tables after test


@pytest.fixture(name="client")
def client_fixture(session: SessionTesting):
    def override_get_db():
        yield session

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()
    
    
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
