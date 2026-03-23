import pytest
import requests

def test_add_wallet_missing_amount(base_url, headers):
    assert requests.post(f"{base_url}/wallet/add", headers=headers, json={}).status_code in [400, 422]

def test_add_wallet_string_amount(base_url, headers):
    assert requests.post(f"{base_url}/wallet/add", headers=headers, json={"amount": "fifty"}).status_code in [400, 422]

def test_add_wallet_boolean_amount(base_url, headers):
    assert requests.post(f"{base_url}/wallet/add", headers=headers, json={"amount": True}).status_code in [400, 422]

def test_add_wallet_float_amount(base_url, headers):
    assert requests.post(f"{base_url}/wallet/add", headers=headers, json={"amount": 50.5}).status_code in [400, 422]

def test_add_wallet_sql_injection_amount(base_url, headers):
    assert requests.post(f"{base_url}/wallet/add", headers=headers, json={"amount": "1; DROP TABLE wallet;"}).status_code in [400, 422]
