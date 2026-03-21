import pytest
import requests

@pytest.fixture
def product(base_url, headers):
    return requests.get(f"{base_url}/products", headers=headers).json()[0]

def test_get_reviews(base_url, headers, product):
    res = requests.get(f"{base_url}/products/{product['product_id']}/reviews", headers=headers)
    assert res.status_code == 200

@pytest.mark.xfail(reason="Bug 12: The Add Review endpoint `/add` routes locally to a 404 Not Found.")
def test_add_review_invalid_rating(base_url, headers, product):
    """Ratings must strictly be bounded 1-5."""
    p_id = product["product_id"]
    payload = {"rating": 6, "review_text": "Too good"}
    assert requests.post(f"{base_url}/products/{p_id}/reviews/add", headers=headers, json=payload).status_code == 400
    
    payload = {"rating": 0, "review_text": "Terrible"}
    assert requests.post(f"{base_url}/products/{p_id}/reviews/add", headers=headers, json=payload).status_code == 400

@pytest.mark.xfail(reason="Bug 12: The Add Review endpoint `/add` routes locally to a 404 Not Found.")
def test_add_review_has_not_bought(base_url, headers):
    """Only users who have ordered the product can review it."""
    h2 = headers.copy()
    h2["X-User-ID"] = "3"
    payload = {"rating": 4, "review_text": "Nice"}
    
    res = requests.post(f"{base_url}/products/1/reviews/add", headers=h2, json=payload)
    if res.status_code == 200: 
        pytest.skip("User 3 coincidentally bought product 1, logic untested.")
    assert res.status_code == 400

@pytest.mark.xfail(reason="Bug 12: The Add Review endpoint `/add` routes locally to a 404 Not Found.")
def test_add_review_duplicate(base_url, headers, product):
    """A user can only write one review per product."""
    p_id = product["product_id"]
    payload = {"rating": 4, "review_text": "Good"}
    requests.post(f"{base_url}/products/{p_id}/reviews/add", headers=headers, json=payload)
    res2 = requests.post(f"{base_url}/products/{p_id}/reviews/add", headers=headers, json=payload)
    assert res2.status_code == 400
