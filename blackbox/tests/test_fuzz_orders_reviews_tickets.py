import pytest
import requests

def test_get_order_invalid_id(base_url, headers):
    assert requests.get(f"{base_url}/orders/999999", headers=headers).status_code in [400, 403, 404]

def test_get_order_string_id(base_url, headers):
    assert requests.get(f"{base_url}/orders/abc", headers=headers).status_code in [400, 404, 422]

def test_get_orders_missing_headers(base_url):
    assert requests.get(f"{base_url}/orders").status_code in [400, 401, 403]

def test_add_review_missing_fields(base_url, headers):
    assert requests.post(f"{base_url}/products/1/reviews/add", headers=headers, json={"rating": 5}).status_code in [400, 404, 422]

def test_add_review_string_rating(base_url, headers):
    assert requests.post(f"{base_url}/products/1/reviews/add", headers=headers, json={"rating": "five", "review_text": "Good"}).status_code in [400, 404, 422]

def test_add_review_sql_injection(base_url, headers):
    res = requests.post(f"{base_url}/products/1/reviews/add", headers=headers, json={"rating": 5, "review_text": "' OR 1=1 --"})
    assert res.status_code < 500

def test_create_ticket_missing_fields(base_url, headers):
    assert requests.post(f"{base_url}/tickets/create", headers=headers, json={"subject": "Help"}).status_code in [400, 404, 422]

def test_create_ticket_empty_strings(base_url, headers):
    res = requests.post(f"{base_url}/tickets/create", headers=headers, json={"subject": "", "description": ""})
    assert res.status_code < 500

def test_create_ticket_wrong_types(base_url, headers):
    assert requests.post(f"{base_url}/tickets/create", headers=headers, json={"subject": True, "description": False}).status_code in [400, 404, 422]
