import pytest
import requests

def test_get_loyalty_points(base_url, headers):
    """Verify that a user can fetch their loyalty points and that it is formatted accurately."""
    resp = requests.get(f"{base_url}/loyalty", headers=headers)
    assert resp.status_code == 200
    data = resp.json()
    assert "loyalty_points" in data
    assert isinstance(data["loyalty_points"], int)
    assert data["loyalty_points"] >= 0
