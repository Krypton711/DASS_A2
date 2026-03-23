import pytest
import requests

def test_get_profile_valid(base_url, headers):
    """Test retrieving profile with valid headers."""
    resp = requests.get(f"{base_url}/profile", headers=headers)
    assert resp.status_code == 200
    data = resp.json()
    assert "name" in data
    assert "phone" in data

def test_get_profile_missing_roll_number(base_url):
    """Test retrieving profile missing X-Roll-Number."""
    headers = {"X-User-ID": "1"}
    resp = requests.get(f"{base_url}/profile", headers=headers)
    assert resp.status_code == 401
    
def test_get_profile_invalid_roll_number(base_url):
    """Test retrieving profile with invalid X-Roll-Number."""
    headers = {"X-Roll-Number": "abc", "X-User-ID": "1"}
    resp = requests.get(f"{base_url}/profile", headers=headers)
    assert resp.status_code == 400

def test_get_profile_missing_user_id(base_url):
    """Test retrieving profile missing X-User-ID."""
    headers = {"X-Roll-Number": "12345"}
    resp = requests.get(f"{base_url}/profile", headers=headers)
    assert resp.status_code == 400

def test_put_profile_valid(base_url, headers):
    """Test updating profile with valid data."""
    payload = {"name": "John Doe", "phone": "1234567890"}
    resp = requests.put(f"{base_url}/profile", headers=headers, json=payload)
    assert resp.status_code == 200
    
    verify = requests.get(f"{base_url}/profile", headers=headers)
    data = verify.json()
    assert data["name"] == "John Doe"
    assert data["phone"] == "1234567890"

def test_put_profile_invalid_name_short(base_url, headers):
    """Test boundary: Name < 2 chars (invalid)."""
    payload = {"name": "A", "phone": "1234567890"}
    resp = requests.put(f"{base_url}/profile", headers=headers, json=payload)
    assert resp.status_code == 400

def test_put_profile_invalid_name_long(base_url, headers):
    """Test boundary: Name > 50 chars (invalid)."""
    payload = {"name": "A" * 51, "phone": "1234567890"}
    resp = requests.put(f"{base_url}/profile", headers=headers, json=payload)
    assert resp.status_code == 400

def test_put_profile_valid_name_boundary(base_url, headers):
    """Test boundary: Name exactly 50 chars (valid)."""
    payload = {"name": "A" * 50, "phone": "1234567890"}
    resp = requests.put(f"{base_url}/profile", headers=headers, json=payload)
    assert resp.status_code == 200

def test_put_profile_invalid_phone_short(base_url, headers):
    """Test boundary: Phone < 10 digits (invalid)."""
    payload = {"name": "John", "phone": "123456789"}
    resp = requests.put(f"{base_url}/profile", headers=headers, json=payload)
    assert resp.status_code == 400

@pytest.mark.xfail(reason="Bug 1: API accepts strings instead of strictly 10-digit numbers.")
def test_put_profile_wrong_datatype_phone(base_url, headers):
    """Test wrong data type for phone field (string with letters)."""
    payload = {"name": "John", "phone": "abcdefghij"}
    resp = requests.put(f"{base_url}/profile", headers=headers, json=payload)
    assert resp.status_code == 400

def test_put_profile_missing_field(base_url, headers):
    """Test missing name field in PUT request."""
    payload = {"phone": "1234567890"}
    resp = requests.put(f"{base_url}/profile", headers=headers, json=payload)
    assert resp.status_code == 400
def test_put_profile_extra_fields(base_url, headers):
    payload = {"name": "Valid", "phone": "1234567890", "is_admin": True, "balance": 9999}
    res = requests.put(f"{base_url}/profile", headers=headers, json=payload)
    assert res.status_code < 500

def test_put_profile_boolean_types(base_url, headers):
    payload = {"name": True, "phone": False}
    assert requests.put(f"{base_url}/profile", headers=headers, json=payload).status_code in [400, 422]

def test_put_profile_empty_json(base_url, headers):
    assert requests.put(f"{base_url}/profile", headers=headers, json={}).status_code in [400, 422]

def test_put_profile_sql_injection(base_url, headers):
    payload = {"name": "' OR 1=1 --", "phone": "1234567890"}
    res = requests.put(f"{base_url}/profile", headers=headers, json=payload)
    assert res.status_code < 500

def test_get_profile_sql_injection_headers(base_url, headers):
    h = headers.copy()
    h["X-User-ID"] = "' DROP TABLE users; --"
    assert requests.get(f"{base_url}/profile", headers=h).status_code in [400, 401]
