import pytest
import requests

def test_get_wallet(base_url, headers):
    """The user can retrieve their current wallet balance."""
    res = requests.get(f"{base_url}/wallet", headers=headers)
    assert res.status_code == 200
    assert "wallet_balance" in res.json()

def test_add_wallet_valid(base_url, headers):
    """Users can add wallet balances safely below thresholds."""
    start = requests.get(f"{base_url}/wallet", headers=headers).json()["wallet_balance"]
    if start > 9900:
        pytest.skip("Wallet balance is organically too high to test addition properly without hitting ceiling caps.")
        
    payload = {"amount": 50}
    res = requests.post(f"{base_url}/wallet/add", headers=headers, json=payload)
    assert res.status_code == 200
    
    end = requests.get(f"{base_url}/wallet", headers=headers).json()["wallet_balance"]
    assert end == start + 50

def test_add_wallet_invalid_amount(base_url, headers):
    """A user cannot add a negative amount or 0."""
    assert requests.post(f"{base_url}/wallet/add", headers=headers, json={"amount": 0}).status_code == 400
    assert requests.post(f"{base_url}/wallet/add", headers=headers, json={"amount": -50}).status_code == 400

@pytest.mark.xfail(reason="Bug 9: System lacks single-deposit threshold enforcement (5000 max).")
def test_add_wallet_exceeds_deposit_limit(base_url, headers):
    """A user cannot add more than 5000 to their wallet at a single time."""
    assert requests.post(f"{base_url}/wallet/add", headers=headers, json={"amount": 5001}).status_code == 400
    
@pytest.mark.xfail(reason="Bug 10: System lacks absolute 10000 global cap verification before crediting.")
def test_add_wallet_exceeds_max_balance(base_url, headers):
    """A user's wallet limit cannot be pushed past 10000 limit across sequential bursts."""
    for _ in range(4):
        res = requests.post(f"{base_url}/wallet/add", headers=headers, json={"amount": 4000})
        if res.status_code == 400:
            break
            
    assert requests.post(f"{base_url}/wallet/add", headers=headers, json={"amount": 4000}).status_code == 400
