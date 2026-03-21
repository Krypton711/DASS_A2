import pytest
import requests

@pytest.fixture
def product(base_url, headers):
    products = requests.get(f"{base_url}/products", headers=headers).json()
    if not products:
        pytest.skip()
    return products[0]

@pytest.fixture
def empty_cart(base_url, headers):
    requests.delete(f"{base_url}/cart/clear", headers=headers)

@pytest.mark.xfail(reason="Bug 4: Subtotal calculation overflows aggressively due to small bit size assignment")
def test_cart_lifecycle(base_url, headers, product, empty_cart):
    p_id = product["product_id"]
    price = product["price"]
    
    # 1. Add item
    payload = {"product_id": p_id, "quantity": 1}
    res = requests.post(f"{base_url}/cart/add", headers=headers, json=payload)
    assert res.status_code == 200
    
    # 2. Add same item (quantity should add up)
    requests.post(f"{base_url}/cart/add", headers=headers, json=payload)
    
    # 3. GET cart and verify totals
    cart = requests.get(f"{base_url}/cart", headers=headers).json()
    item = next(i for i in cart["items"] if i["product_id"] == p_id)
    assert item["quantity"] == 2
    assert item["subtotal"] == 2 * price
    assert cart["total"] == sum(x["subtotal"] for x in cart["items"])
    
    # 4. Update quantity
    upd_payload = {"product_id": p_id, "quantity": 5}
    requests.post(f"{base_url}/cart/update", headers=headers, json=upd_payload)
    
    cart = requests.get(f"{base_url}/cart", headers=headers).json()
    item = next(i for i in cart["items"] if i["product_id"] == p_id)
    assert item["quantity"] == 5
    assert item["subtotal"] == 5 * price
    
    # 5. Remove item
    rem_payload = {"product_id": p_id}
    res = requests.post(f"{base_url}/cart/remove", headers=headers, json=rem_payload)
    assert res.status_code == 200
    
    cart = requests.get(f"{base_url}/cart", headers=headers).json()
    assert not any(i["product_id"] == p_id for i in cart["items"])

@pytest.mark.xfail(reason="Bug 5: API allows quantities of 0 and negative inputs.")
def test_cart_add_invalid_quantity(base_url, headers, product, empty_cart):
    """When adding an item, the quantity must be at least 1."""
    p_id = product["product_id"]
    payload = {"product_id": p_id, "quantity": 0}
    res = requests.post(f"{base_url}/cart/add", headers=headers, json=payload)
    assert res.status_code == 400
    
    payload["quantity"] = -5
    res = requests.post(f"{base_url}/cart/add", headers=headers, json=payload)
    assert res.status_code == 400

def test_cart_add_invalid_product(base_url, headers):
    payload = {"product_id": 999999, "quantity": 1}
    res = requests.post(f"{base_url}/cart/add", headers=headers, json=payload)
    assert res.status_code == 404

def test_cart_remove_nonexistent(base_url, headers):
    payload = {"product_id": 999999}
    res = requests.post(f"{base_url}/cart/remove", headers=headers, json=payload)
    assert res.status_code == 404
    
def test_cart_add_exceeds_stock(base_url, headers, product, empty_cart):
    p_id = product["product_id"]
    payload = {"product_id": p_id, "quantity": 99999999}
    res = requests.post(f"{base_url}/cart/add", headers=headers, json=payload)
    assert res.status_code == 400
