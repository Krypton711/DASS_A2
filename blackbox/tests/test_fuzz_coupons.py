import pytest
import requests

def test_apply_nonexistent_coupon(base_url, headers):
    assert requests.post(f"{base_url}/coupon/apply", headers=headers, json={"coupon_code": "NONEXISTENT99"}).status_code in [400, 404]

def test_apply_missing_coupon_field(base_url, headers):
    assert requests.post(f"{base_url}/coupon/apply", headers=headers, json={}).status_code in [400, 422]

def test_remove_empty_coupon(base_url, headers):
    requests.post(f"{base_url}/coupon/remove", headers=headers)
    res = requests.post(f"{base_url}/coupon/remove", headers=headers)
    assert res.status_code in [200, 204, 400]

def test_apply_sql_injection_coupon(base_url, headers):
    res = requests.post(f"{base_url}/coupon/apply", headers=headers, json={"coupon_code": "' OR '1'='1"})
    assert res.status_code < 500

def test_apply_coupon_wrong_type(base_url, headers):
    assert requests.post(f"{base_url}/coupon/apply", headers=headers, json={"coupon_code": 12345}).status_code in [400, 422]
