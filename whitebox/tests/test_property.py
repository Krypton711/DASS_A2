import pytest
from moneypoly.property import Property, PropertyGroup
from moneypoly.player import Player

def test_property_rent_calculation():
    """Test rent logic including mortgaged state and full group ownership."""
    player1 = Player("P1")
    player2 = Player("P2")
    group = PropertyGroup("Test", "blue")
    
    prop1 = Property("Prop1", 1, 100, 10)
    prop2 = Property("Prop2", 2, 100, 10)
    group.add_property(prop1)
    group.add_property(prop2)
    
    prop1.owner = player1
    prop2.owner = player2
    
    # Not fully owned by player1, since player2 owns prop2
    # Should just return base_rent
    assert prop1.get_rent() == 10
    
    # Now player1 owns both, full group!
    prop2.owner = player1
    assert prop1.get_rent() == 20
    
    # Mortgaged property yields 0 rent
    prop1.mortgage()
    assert prop1.get_rent() == 0

def test_property_mortgage_unmortgage():
    """Test mortgage lifecycle and cost calculations."""
    prop = Property("Prop", 1, 200, 20)
    assert prop.mortgage_value == 100
    
    assert prop.unmortgage() == 0 # Already unmortgaged
    
    payout = prop.mortgage()
    assert payout == 100
    assert prop.is_mortgaged is True
    
    assert prop.mortgage() == 0 # Already mortgaged
    
    cost = prop.unmortgage()
    assert cost == 110 # 10% interest
    assert prop.is_mortgaged is False
    
def test_property_is_available():
    """Test when property is purchasable."""
    player = Player("P1")
    prop = Property("Prop", 1, 100, 10)
    
    assert prop.is_available() is True
    
    prop.owner = player
    assert prop.is_available() is False
    
    prop.owner = None
    prop.mortgage()
    assert prop.is_available() is False
