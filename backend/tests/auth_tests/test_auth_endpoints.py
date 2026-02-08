"""
Authentication tests for the Todo API
These tests verify that authentication works correctly
"""
import pytest
from fastapi.testclient import TestClient
from src.main import app


@pytest.fixture
def client():
    """Test client for the FastAPI app"""
    # Clear any dependency overrides to test real auth
    app.dependency_overrides.clear()
    return TestClient(app)


def test_unauthenticated_requests_return_401(client):
    """Test that unauthenticated requests return 401 Unauthorized"""
    # Test various endpoints that should require authentication
    # Routes use /api/{user_id}/tasks pattern (no /users/ prefix)
    endpoints_to_test = [
        "/api/testuser/tasks",
    ]

    for endpoint in endpoints_to_test:
        response = client.get(endpoint)
        assert response.status_code in [401, 403], f"Expected 401/403 for GET {endpoint}, got {response.status_code}"


def test_unauthenticated_post_returns_401(client):
    """Test that unauthenticated POST requests return 401/422"""
    response = client.post(
        "/api/testuser/tasks",
        json={"title": "Test", "description": "Test"}
    )
    # Without auth header, FastAPI returns 403 (HTTPBearer scheme)
    assert response.status_code in [401, 403], f"Expected 401/403 for POST, got {response.status_code}"


def test_valid_jwt_authentication(client):
    """Test that valid JWT tokens allow access to protected endpoints"""
    # This test would require a valid JWT token to be created and used
    # For now, we'll add a placeholder
    pass
