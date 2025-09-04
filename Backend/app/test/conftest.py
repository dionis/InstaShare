import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from core.main import app, get_document_service, get_user_service, get_role_service, get_log_service
from db.base import Base, get_db, get_supabase_client

from unittest.mock import AsyncMock
from core.main import app
from services.document_service import DocumentService
from services.user_service import UserService
from services.role_service import RoleService
from services.log_service import LogService
from auth.jwt import create_access_token, Token
from schemas.user import UserCreate

from supabase import Client
from datetime import datetime
from models import User

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
def mock_supabase_client():
    mock_client = AsyncMock(spec=Client)
    app.dependency_overrides[get_supabase_client] = lambda: mock_client
    yield mock_client
    app.dependency_overrides = {}

@pytest.fixture(name="dummy_user")
def dummy_user_fixture():
    # In a real scenario, you might hash the password
    return {
        "id": 1,
        "username": "Test User",
        "email": "test@example.com",
        "password": "testpassword",
        "hashed_password": "testpassword",
        "phone": "1234567890",
        "responsability": "User",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
        "deleted_at": None
    }

@pytest.fixture(name="authenticated_client")
def authenticated_client_fixture(client: TestClient, mock_supabase_client: AsyncMock, dummy_user: dict, session: SessionTesting):
    # Add the dummy user to the session
    user_model = User(**dummy_user)
    session.add(user_model)
    session.commit()
    session.refresh(user_model)

    # Mock the user query in the Supabase client mock
    mock_supabase_client.from_.return_value.select.return_value.eq.return_value.is_.return_value.execute.return_value.data = [dummy_user]
    
    access_token = create_access_token(data={"sub": dummy_user["email"]})
    
    client.headers = {
        "Authorization": f"Bearer {access_token}"
    }
    yield client
    client.headers = {}

@pytest.fixture
def mock_document_service(mock_supabase_client):
    service = AsyncMock(spec=DocumentService)
    service.supabase = mock_supabase_client # Ensure mock_supabase_client is accessible if needed
    app.dependency_overrides[get_document_service] = lambda: service
    yield service
    app.dependency_overrides = {}

@pytest.fixture
def mock_user_service(mock_supabase_client):
    service = AsyncMock(spec=UserService)
    service.supabase = mock_supabase_client # Ensure mock_supabase_client is accessible if needed
    app.dependency_overrides[get_user_service] = lambda: service
    yield service
    app.dependency_overrides = {}

@pytest.fixture
def mock_role_service(mock_supabase_client):
    service = AsyncMock(spec=RoleService)
    service.supabase = mock_supabase_client # Ensure mock_supabase_client is accessible if needed
    app.dependency_overrides[get_role_service] = lambda: service
    yield service
    app.dependency_overrides = {}

@pytest.fixture
def mock_log_service(mock_supabase_client):
    service = AsyncMock(spec=LogService)
    service.supabase = mock_supabase_client # Ensure mock_supabase_client is accessible if needed
    app.dependency_overrides[get_log_service] = lambda: service
    yield service
    app.dependency_overrides = {}
