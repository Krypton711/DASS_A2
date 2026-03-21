import pytest
import requests
import random
import string

@pytest.mark.xfail(reason="Bug 13: Support Tickets API endpoints return 404 unconditionally, missing architecture.")
def test_get_tickets(base_url, headers):
    res = requests.get(f"{base_url}/tickets", headers=headers)
    assert res.status_code == 200

@pytest.mark.xfail(reason="Bug 13: Support Tickets API endpoints return 404 unconditionally, missing architecture.")
def test_create_ticket_status(base_url, headers):
    """A new ticket should securely start as OPEN."""
    payload = {"subject": "Help", "description": "Issue details"}
    res = requests.post(f"{base_url}/tickets/create", headers=headers, json=payload)
    assert res.status_code == 200
    assert res.json().get("status") == "OPEN"

@pytest.mark.xfail(reason="Bug 13: Support Tickets API endpoints return 404 unconditionally, missing architecture.")
def test_create_ticket_exceeds_max_open(base_url, headers):
    """A user can have at most 3 OPEN tickets at the same time."""
    for _ in range(3):
        txt = ''.join(random.choices(string.ascii_letters, k=5))
        requests.post(f"{base_url}/tickets/create", headers=headers, json={"subject": txt, "description": txt})
        
    res = requests.post(f"{base_url}/tickets/create", headers=headers, json={"subject": "Limit", "description": "Exceeded"})
    assert res.status_code == 400
