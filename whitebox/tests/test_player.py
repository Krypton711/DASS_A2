import pytest
from moneypoly.player import Player
from moneypoly.property import Property

def test_player_money_management():
    """Test adding/deducting money and bankruptcy."""
    player = Player("P1", balance=100)
    
    with pytest.raises(ValueError):
        player.add_money(-10)
    with pytest.raises(ValueError):
        player.deduct_money(-10)
        
    player.add_money(50)
    assert player.balance == 150
    assert player.is_bankrupt() is False
    
    player.deduct_money(150)
    assert player.balance == 0
    assert player.is_bankrupt() is True

def test_player_movement_and_go():
    """Test standard movement and the bounds for passing GO."""
    from moneypoly.config import GO_SALARY
    player = Player("P1", balance=0)
    
    # Move normally
    pos = player.move(5)
    assert pos == 5
    assert player.position == 5
    assert player.balance == 0
    
    # Move past GO (from 38 to 2)
    player.position = 38
    player.move(4)
    assert player.position == 2
    assert player.balance == GO_SALARY # Collected GO_SALARY
    
    # Land exactly on GO
    player.position = 35
    player.move(5)
    assert player.position == 0
    assert player.balance == GO_SALARY * 2

def test_player_properties():
    """Test adding and removing properties."""
    player = Player("P1")
    prop = Property("Prop", 1, 100, 10)
    
    assert player.count_properties() == 0
    
    player.add_property(prop)
    assert player.count_properties() == 1
    
    # Add again shouldn't duplicate
    player.add_property(prop)
    assert player.count_properties() == 1
    
    player.remove_property(prop)
    assert player.count_properties() == 0
    
    # Remove again shouldn't crash
    player.remove_property(prop)
    assert player.count_properties() == 0

def test_player_net_worth():
    """Test net worth includes balance, unmortgaged properties (full price) and mortgaged properties (mortgage value)."""
    player = Player("P1", balance=100)
    prop1 = Property("P1", 1, 200, 20)
    prop2 = Property("P2", 2, 300, 30)
    
    player.add_property(prop1)
    player.add_property(prop2)
    
    payout = prop2.mortgage()
    player.add_money(payout)
    
    # balance = 100 + 150 (from mortgage) = 250
    # prop1 (unmortgaged) = 200
    # prop2 (mortgaged) = 150
    # total net worth = 250 + 200 + 150 = 600
    assert player.net_worth() == 600
