import pytest
import requests

@pytest.fixture
def empty_cart(base_url, headers):
    requests.delete(f"{base_url}/cart/clear", headers=headers)

@pytest.fixture
def cart_setup(base_url, headers):
    requests.delete(f"{base_url}/cart/clear", headers=headers)
    products = requests.get(f"{base_url}/products", headers=headers).json()
    requests.post(f"{base_url}/cart/add", headers=headers, json={"product_id": products[0]["product_id"], "quantity": 1})
    item_price = products[0]["price"]
    return item_price

@pytest.fixture
def address(base_url, headers):
    payload = {"label": "HOME", "street": "123 Test St", "city": "TestCity", "pincode": "123456", "is_default": True}
    requests.post(f"{base_url}/addresses", headers=headers, json=payload)
    arr = requests.get(f"{base_url}/addresses", headers=headers).json()
    return arr[0]["address_id"]

def test_checkout_empty_cart(base_url, headers, empty_cart, address):
    """The cart must not be empty."""
    payload = {"payment_method": "CARD", "address_id": address}
    res = requests.post(f"{base_url}/checkout", headers=headers, json=payload)
    assert res.status_code == 400

def test_checkout_invalid_payment(base_url, headers, cart_setup, address):
    """Payment methods besides COD, WALLET, CARD are rejected"""
    payload = {"payment_method": "CASH", "address_id": address}
    res = requests.post(f"{base_url}/checkout", headers=headers, json=payload)
    assert res.status_code == 400

def test_checkout_cod_limit(base_url, headers, address):
    """COD is not allowed if the order total is more than 5000."""
    requests.delete(f"{base_url}/cart/clear", headers=headers)
    products = requests.get(f"{base_url}/products", headers=headers).json()
    requests.post(f"{base_url}/cart/add", headers=headers, json={"product_id": products[0]["product_id"], "quantity": 1000}) # Artificially spiking cart
    
    payload = {"payment_method": "COD", "address_id": address}
    res = requests.post(f"{base_url}/checkout", headers=headers, json=payload)
    assert res.status_code == 400

def test_checkout_card_status(base_url, headers, cart_setup, address):
    """When paying with CARD, order starts as PAID."""
    payload = {"payment_method": "CARD", "address_id": address}
    res = requests.post(f"{base_url}/checkout", headers=headers, json=payload)
    assert res.status_code == 200
    assert res.json().get("payment_status") == "PAID"
    
    # Check GST math logic = +5%
    expected = cart_setup * 1.05
    assert res.json().get("total_amount") == expected

@pytest.mark.xfail(reason="Bug 8: COD payments mistakenly marked as PAID instead of PENDING.")
def test_checkout_cod_status(base_url, headers, cart_setup, address):
    """When paying with COD, it starts as PENDING."""
    payload = {"payment_method": "COD", "address_id": address}
    res = requests.post(f"{base_url}/checkout", headers=headers, json=payload)
    assert res.status_code == 200
    assert res.json().get("payment_status") == "PENDING"
