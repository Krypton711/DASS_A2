import pytest
import requests

def test_put_address_invalid_id(base_url, headers):
    res = requests.put(f"{base_url}/addresses/99999", headers=headers, json={"label": "HOME", "street": "Road", "city": "City", "pincode": "123456"})
    assert res.status_code in [400, 404]

def test_delete_address_invalid_id(base_url, headers):
    assert requests.delete(f"{base_url}/addresses/99999", headers=headers).status_code in [400, 404]

def test_post_address_missing_fields(base_url, headers):
    assert requests.post(f"{base_url}/addresses", headers=headers, json={"label": "HOME"}).status_code in [400, 422]

def test_post_address_sql_injection(base_url, headers):
    res = requests.post(f"{base_url}/addresses", headers=headers, json={"label": "HOME", "street": "' OR 1=1 --", "city": "City", "pincode": "123456"})
    assert res.status_code < 500

def test_post_address_wrong_types(base_url, headers):
    res = requests.post(f"{base_url}/addresses", headers=headers, json={"label": True, "street": False, "city": 123, "pincode": 123456})
    assert res.status_code in [400, 422]
