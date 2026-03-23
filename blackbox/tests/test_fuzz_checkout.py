import pytest
import requests

def test_checkout_missing_fields(base_url, headers):
    assert requests.post(f"{base_url}/checkout", headers=headers, json={}).status_code in [400, 422]

def test_checkout_invalid_address_id(base_url, headers):
    assert requests.post(f"{base_url}/checkout", headers=headers, json={"payment_method": "COD", "address_id": 99999}).status_code in [400, 404]

def test_checkout_string_address_id(base_url, headers):
    assert requests.post(f"{base_url}/checkout", headers=headers, json={"payment_method": "COD", "address_id": "home"}).status_code in [400, 422]

def test_checkout_sql_injection_payment(base_url, headers):
    res = requests.post(f"{base_url}/checkout", headers=headers, json={"payment_method": "' OR 1=1 --", "address_id": 1})
    assert res.status_code < 500

def test_checkout_boolean_payment(base_url, headers):
    assert requests.post(f"{base_url}/checkout", headers=headers, json={"payment_method": True, "address_id": 1}).status_code in [400, 422]
