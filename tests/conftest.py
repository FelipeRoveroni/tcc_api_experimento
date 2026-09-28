import pytest
from fastapi.testclient import TestClient

from app.main import app, repository


@pytest.fixture()
def client():
    repository.reset()
    with TestClient(app) as test_client:
        yield test_client
