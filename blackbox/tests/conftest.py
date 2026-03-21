import pytest
import requests

@pytest.fixture
def base_url():
    return "http://localhost:8080/api/v1"

@pytest.fixture
def base_headers():
    return {
        "X-Roll-Number": "20261234",
    }

@pytest.fixture
def headers(base_headers):
    # User 1 should exist based on standard DB implementations
    headers_with_user = base_headers.copy()
    headers_with_user["X-User-ID"] = "1"
    return headers_with_user

@pytest.fixture
def session(headers):
    session = requests.Session()
    session.headers.update(headers)
    return session
