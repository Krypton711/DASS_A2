import pytest
import requests
from datetime import datetime, timezone

def is_expired(c):
    exp = datetime.fromisoformat(c["expiry_date"].replace("Z", "+00:00"))
    return exp < datetime.now(timezone.utc)

@pytest.fixture
def get_coupons(base_url, headers):
    resp = requests.get(f"{base_url}/admin/coupons", headers={"X-Roll-Number": headers["X-Roll-Number"]})
    return resp.json()

@pytest.fixture
def product(base_url, headers):
    products = requests.get(f"{base_url}/products", headers=headers).json()
    return products[0]

@pytest.fixture
def cart_setup(base_url, headers, product):
    requests.delete(f"{base_url}/cart/clear", headers=headers)
    requests.post(f"{base_url}/cart/add", headers=headers, json={"product_id": product["product_id"], "quantity": 1})
    return requests.get(f"{base_url}/cart", headers=headers).json()

@pytest.mark.xfail(reason="Bug 7: Discount value missing from API cart payload entirely.")
def test_apply_valid_fixed_coupon(base_url, headers, get_coupons, cart_setup):
    """Applying a valid FIXED coupon must reduce total flatly."""
    valid_c = next((c for c in get_coupons if not is_expired(c) and c.get("min_cart_value", 0) <= 120 and c["discount_type"] == "FIXED"), None)
    if not valid_c:
        pytest.skip("No FIXED coupons available for this cart setup")
        
    code = valid_c["coupon_code"]
    res = requests.post(f"{base_url}/coupon/apply", headers=headers, json={"coupon_code": code})
    assert res.status_code == 200
    
    cart = requests.get(f"{base_url}/cart", headers=headers).json()
    assert cart.get("discount") == valid_c["discount_value"]
    
@pytest.mark.xfail(reason="Bug 7: Discount value missing from API cart payload entirely.")
def test_apply_valid_percent_coupon(base_url, headers, get_coupons, cart_setup):
    """PERCENT coupon takes a percentage off the total, strictly capping below max_discount."""
    pct_c = next((c for c in get_coupons if c["discount_type"] == "PERCENT" and not is_expired(c) and c.get("min_cart_value", 0) <= 120), None)
    if not pct_c:
        pytest.skip("No PERCENT coupons available for this cart setup")
        
    code = pct_c["coupon_code"]
    res = requests.post(f"{base_url}/coupon/apply", headers=headers, json={"coupon_code": code})
    assert res.status_code == 200
    
    cart = requests.get(f"{base_url}/cart", headers=headers).json()
    expected_discount = (120 * pct_c["discount_value"]) / 100
    if pct_c.get("max_discount", 0) > 0:
        expected_discount = min(expected_discount, pct_c["max_discount"])
        
    assert cart.get("discount") == expected_discount

def test_apply_expired_coupon(base_url, headers, get_coupons, cart_setup):
    """The coupon must not be expired."""
    expired_c = next((c for c in get_coupons if is_expired(c)), None)
    if not expired_c:
        pytest.skip("No expired coupons found")
        
    code = expired_c["coupon_code"]
    res = requests.post(f"{base_url}/coupon/apply", headers=headers, json={"coupon_code": code})
    assert res.status_code == 400

def test_apply_min_value_unmet(base_url, headers, get_coupons):
    """Cart total must strictly meet the coupon's minimum cart value."""
    requests.delete(f"{base_url}/cart/clear", headers=headers) # Empty cart => total 0
    high_min_c = next((c for c in get_coupons if c.get("min_cart_value", 0) > 0), None)
    if not high_min_c:
        pytest.skip("No coupons with minimum constraints")
        
    code = high_min_c["coupon_code"]
    res = requests.post(f"{base_url}/coupon/apply", headers=headers, json={"coupon_code": code})
    assert res.status_code == 400

def test_remove_coupon(base_url, headers, get_coupons, cart_setup):
    """Removal resets the active discount flag to 0."""
    valid_c = next((c for c in get_coupons if not is_expired(c)), None)
    if not valid_c:
        pytest.skip("No valid coupons")
    
    code = valid_c["coupon_code"]
    requests.post(f"{base_url}/coupon/apply", headers=headers, json={"coupon_code": code})
    res = requests.post(f"{base_url}/coupon/remove", headers=headers)
    assert res.status_code == 200
    
    cart = requests.get(f"{base_url}/cart", headers=headers).json()
    assert cart.get("discount", 0) == 0
