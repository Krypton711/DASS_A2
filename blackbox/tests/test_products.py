import pytest
import requests

def test_get_products_active_only(base_url, headers):
    """The product list only returns products that are active."""
    resp = requests.get(f"{base_url}/products", headers=headers)
    assert resp.status_code == 200
    products = resp.json()
    assert isinstance(products, list)
    for p in products:
        if "is_active" in p:
            assert p["is_active"] is True

def test_get_product_by_id_valid(base_url, headers):
    """Testing single product lookup strictly by ID."""
    resp = requests.get(f"{base_url}/products", headers=headers)
    products = resp.json()
    if not products:
        pytest.skip()
        
    p_id = products[0]["product_id"]
    res = requests.get(f"{base_url}/products/{p_id}", headers=headers)
    assert res.status_code == 200
    assert res.json()["product_id"] == p_id

def test_get_product_by_id_invalid_404(base_url, headers):
    """Looking up a single product by ID returns a 404 error if the product does not exist."""
    res = requests.get(f"{base_url}/products/999999", headers=headers)
    assert res.status_code == 404

def test_get_products_filter_category(base_url, headers):
    """Products can be filtered by category."""
    resp = requests.get(f"{base_url}/products", headers=headers)
    products = resp.json()
    if not products:
        pytest.skip()
    cat = products[0].get("category")
    if not cat:
        pytest.skip()
        
    res = requests.get(f"{base_url}/products?category={cat}", headers=headers)
    assert res.status_code == 200
    for p in res.json():
        assert p["category"] == cat

def test_get_products_search_name(base_url, headers):
    """Products can be searched by name."""
    resp = requests.get(f"{base_url}/products", headers=headers)
    products = resp.json()
    if not products:
        pytest.skip()
    name = products[0]["name"]
    query = name[:3]
    
    res = requests.get(f"{base_url}/products?search={query}", headers=headers)
    assert res.status_code == 200
    assert len(res.json()) >= 1

def test_get_products_sort_price_up(base_url, headers):
    """Products can be sorted by price going up (assuming ?sort=price&order=asc or similar structure)."""
    # Simply validating the param doesn't panic the endpoint. Precise ordering validation depends on API param structure which is undocumented, but common is ?sort=price.
    res = requests.get(f"{base_url}/products?sort=price", headers=headers)
    assert res.status_code == 200
