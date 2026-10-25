import pytest
from fastapi.testclient import TestClient

from calculator.main import app

API_PREFIX = "/api/v1/calculate"


@pytest.fixture
def client():
    # raise_server_exceptions=False so an unhandled error shows up as a 500
    # response instead of crashing the test, which is what a real client would see.
    with TestClient(app, raise_server_exceptions=False) as test_client:
        yield test_client
