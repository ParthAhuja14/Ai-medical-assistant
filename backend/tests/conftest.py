import os
import sys
import tempfile
import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Use a throwaway SQLite file for tests so we never touch dev/prod data.
TEST_DB_FD, TEST_DB_PATH = tempfile.mkstemp(suffix=".db")
os.environ["DATABASE_URL"] = f"sqlite:///{TEST_DB_PATH}"
os.environ["SECRET_KEY"] = "test-secret-key-not-for-production"

from app.main import app  # noqa: E402


@pytest.fixture(scope="session")
def client():
    with TestClient(app) as c:
        yield c
    os.close(TEST_DB_FD)
    os.remove(TEST_DB_PATH)


@pytest.fixture
def auth_headers(client):
    """Registers a fresh user and returns Authorization headers for them."""
    import uuid
    email = f"test-{uuid.uuid4().hex[:8]}@example.com"
    resp = client.post("/api/auth/register", json={
        "full_name": "Test User",
        "email": email,
        "password": "password123",
    })
    assert resp.status_code == 201, resp.text
    token = resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
