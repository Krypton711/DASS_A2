import pytest
from moneypoly.bank import Bank
from moneypoly.player import Player

def test_give_loan_reduces_funds():
    """Test that issuing a loan correctly reduces bank funds and updates history."""
    bank = Bank()
    player = Player("Alice", balance=0)
    initial_funds = bank.get_balance()
    
    bank.give_loan(player, 500)
    
    assert player.balance == 500
    assert bank.get_balance() == initial_funds - 500
    assert bank.loan_count() == 1
    assert bank.total_loans_issued() == 500

def test_payout_insufficient_funds():
    """Test that paying out more than available funds raises ValueError."""
    bank = Bank()
    available = bank.get_balance()
    with pytest.raises(ValueError):
        bank.pay_out(available + 10)

def test_negative_payout_and_loan():
    """Test that zero or negative amounts return early with no effect."""
    bank = Bank()
    player = Player("Bob", balance=0)
    
    assert bank.pay_out(-50) == 0
    assert bank.pay_out(0) == 0
    
    bank.give_loan(player, -50)
    bank.give_loan(player, 0)
    
    assert player.balance == 0
    assert bank.loan_count() == 0

def test_collect_funds():
    """Test that collecting funds works correctly."""
    bank = Bank()
    initial = bank.get_balance()
    bank.collect(100)
    assert bank.get_balance() == initial + 100
