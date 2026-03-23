import pytest
import requests

ENDPOINTS = [
    "/profile",
    "/addresses",
    "/products",
    "/cart",
    "/wallet",
    "/loyalty",
    "/orders",
    "/tickets",
    "/products/1/reviews"
]

@pytest.mark.xfail(reason="Bug 14: Global Authentication Enforcement Failure")
@pytest.mark.parametrize("endpoint", ENDPOINTS)
def test_missing_roll_number(base_url, endpoint):
    """Missing X-Roll-Number should strictly return a 401 error."""
    res = requests.get(f"{base_url}{endpoint}", headers={"X-User-ID": "1"})
    assert res.status_code == 401

@pytest.mark.xfail(reason="Bug 14: Global Authentication Enforcement Failure")
@pytest.mark.parametrize("endpoint", ENDPOINTS)
def test_invalid_roll_number_type(base_url, endpoint):
    """Invalid string X-Roll-Number should strictly return a 400 error."""
    res = requests.get(f"{base_url}{endpoint}", headers={"X-Roll-Number": "invalid_chars", "X-User-ID": "1"})
    assert res.status_code == 400

@pytest.mark.xfail(reason="Bug 14: Global Authentication Enforcement Failure")
@pytest.mark.parametrize("endpoint", ENDPOINTS)
def test_missing_user_id(base_url, endpoint):
    """Missing X-User-ID on user-scoped routes should strictly return 400 error."""
    res = requests.get(f"{base_url}{endpoint}", headers={"X-Roll-Number": "123456"})
    assert res.status_code == 400

@pytest.mark.xfail(reason="Bug 14: Global Authentication Enforcement Failure")
@pytest.mark.parametrize("endpoint", ENDPOINTS)
def test_invalid_user_id_type(base_url, endpoint):
    """Invalid string X-User-ID should strictly return a 400 error."""
    res = requests.get(f"{base_url}{endpoint}", headers={"X-Roll-Number": "123456", "X-User-ID": "abc"})
    assert res.status_code == 400

@pytest.mark.xfail(reason="Bug 14: Global Authentication Enforcement Failure")
def test_admin_missing_roll_number(base_url):
    """Admin missing Roll Number returns 401."""
    assert requests.get(f"{base_url}/admin/coupons").status_code == 401
    
@pytest.mark.xfail(reason="Bug 14: Global Authentication Enforcement Failure")
def test_admin_invalid_roll_number(base_url):
    """Admin invalid string Roll Number returns 400."""
    assert requests.get(f"{base_url}/admin/coupons", headers={"X-Roll-Number": "abc"}).status_code == 400
