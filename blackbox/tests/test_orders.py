import pytest
import requests

def test_get_orders(base_url, headers):
    res = requests.get(f"{base_url}/orders", headers=headers)
    assert res.status_code == 200
    assert isinstance(res.json(), list)

def test_get_order_by_id(base_url, headers):
    orders = requests.get(f"{base_url}/orders", headers=headers).json()
    if not orders:
        pytest.skip()
    order_id = orders[0]["order_id"]
    res = requests.get(f"{base_url}/orders/{order_id}", headers=headers)
    assert res.status_code == 200
    data = res.json()
    assert "items" in data
    assert "total_amount" in data

@pytest.mark.xfail(reason="Bug 11: Viewing another user's order returns 404 strictly instead of 403 Forbidden.")
def test_get_other_user_order_forbidden(base_url, headers):
    """Attempting to view another user's order must return a 403 error."""
    orders = requests.get(f"{base_url}/orders", headers=headers).json()
    if not orders:
        pytest.skip()
    order_id = orders[0]["order_id"]
    
    h2 = headers.copy()
    h2["X-User-ID"] = "2" # User 2 maliciously attempting to view user 1's order
    res = requests.get(f"{base_url}/orders/{order_id}", headers=h2)
    assert res.status_code == 403
