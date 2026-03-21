import pytest
import requests

def test_address_lifecycle(base_url, headers):
    # 1. POST valid address
    payload = {"label": "HOME", "street": "123 Main St", "city": "Springfield", "pincode": "123456", "is_default": True}
    res = requests.post(f"{base_url}/addresses", headers=headers, json=payload)
    assert res.status_code == 200
    addr = res.json()["address"]
    assert "address_id" in addr
    assert addr["label"] == "HOME"
    
    # 2. GET addresses (should contain custom)
    res = requests.get(f"{base_url}/addresses", headers=headers)
    assert res.status_code == 200
    assert len(res.json()) > 0
    
    # 3. PUT address (change street, is_default)
    update_payload = {"street": "456 New St", "is_default": False, "city": "IgnoredCity", "label": "OFFICE", "pincode": "000000"}
    res = requests.put(f"{base_url}/addresses/{addr['address_id']}", headers=headers, json=update_payload)
    assert res.status_code == 200
    updated = res.json()
    if "address" in updated:
        updated = updated["address"]
    assert updated["street"] == "456 New St"
    assert updated["is_default"] == False
    
    # Validate ignored fields were actually ignored by the server!
    assert updated["city"] == "Springfield"
    assert updated["label"] == "HOME"
    assert updated["pincode"] == "123456"
    
    # 4. DELETE address
    res = requests.delete(f"{base_url}/addresses/{addr['address_id']}", headers=headers)
    assert res.status_code == 200
    
    # 5. DELETE again -> 404
    res = requests.delete(f"{base_url}/addresses/{addr['address_id']}", headers=headers)
    assert res.status_code == 404

def test_post_address_invalid_label(base_url, headers):
    payload = {"label": "CABIN", "street": "123 Main St", "city": "Springfield", "pincode": "123456"}
    res = requests.post(f"{base_url}/addresses", headers=headers, json=payload)
    assert res.status_code == 400

def test_post_address_boundary_street(base_url, headers):
    # Short
    payload = {"label": "HOME", "street": "1234", "city": "Springfield", "pincode": "123456"}
    assert requests.post(f"{base_url}/addresses", headers=headers, json=payload).status_code == 400
    
    # Long
    payload["street"] = "A" * 101
    assert requests.post(f"{base_url}/addresses", headers=headers, json=payload).status_code == 400

@pytest.mark.xfail(reason="Bug 2: API accepts non-numeric pincodes.")
def test_post_address_invalid_pincode(base_url, headers):
    payload = {"label": "HOME", "street": "123 Main St", "city": "Springfield", "pincode": "123"}
    assert requests.post(f"{base_url}/addresses", headers=headers, json=payload).status_code == 400
    
    payload["pincode"] = "abcdef"
    assert requests.post(f"{base_url}/addresses", headers=headers, json=payload).status_code == 400

@pytest.mark.xfail(reason="Bug 3: Old default addresses aren't stripped of their default status")
def test_post_address_default_override(base_url, headers):
    """When a new address is added as the default, all other addresses must stop being the default first."""
    p1 = {"label": "HOME", "street": "Street 1", "city": "City", "pincode": "111111", "is_default": True}
    res1 = requests.post(f"{base_url}/addresses", headers=headers, json=p1).json()
    a1_id = res1["address"]["address_id"]
    
    p2 = {"label": "OFFICE", "street": "Street 2", "city": "City", "pincode": "222222", "is_default": True}
    res2 = requests.post(f"{base_url}/addresses", headers=headers, json=p2).json()
    a2_id = res2["address"]["address_id"]
    
    # Check GET
    arr = requests.get(f"{base_url}/addresses", headers=headers).json()
    first = next(a for a in arr if a["address_id"] == a1_id)
    second = next(a for a in arr if a["address_id"] == a2_id)
    
    assert first["is_default"] is False
    assert second["is_default"] is True
