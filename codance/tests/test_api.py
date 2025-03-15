from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.core.database import Base, get_db
from app.core.init_db import create_initial_admin

# Create an in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override the get_db dependency
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(scope="function")
def test_db():
    # Create the database tables
    Base.metadata.create_all(bind=engine)
    
    # Create a test admin user
    db = TestingSessionLocal()
    create_initial_admin(db)
    db.close()
    
    yield
    
    # Drop the database tables
    Base.metadata.drop_all(bind=engine)

def test_root_endpoint():
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "Codance API" in data["message"]

def test_health_check():
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"

def test_login(test_db):
    """Test user login."""
    response = client.post(
        "/api/v1/users/token",
        data={"username": "admin", "password": "admin123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_invalid_credentials(test_db):
    """Test login with invalid credentials."""
    response = client.post(
        "/api/v1/users/token",
        data={"username": "admin", "password": "wrongpassword"}
    )
    assert response.status_code == 401

def test_protected_endpoint_without_token(test_db):
    """Test accessing a protected endpoint without a token."""
    response = client.get("/api/v1/users/me")
    assert response.status_code == 401

def test_protected_endpoint_with_token(test_db):
    """Test accessing a protected endpoint with a valid token."""
    # First, get a token
    login_response = client.post(
        "/api/v1/users/token",
        data={"username": "admin", "password": "admin123"}
    )
    token = login_response.json()["access_token"]
    
    # Then use the token to access a protected endpoint
    response = client.get(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "admin"
    assert data["is_admin"] == True 