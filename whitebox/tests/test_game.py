import pytest
from unittest.mock import patch
from moneypoly.game import Game
from moneypoly.property import Property

def test_game_buy_property():
    """Test purchasing property branches."""
    game = Game(["P1"])
    player = game.players[0]
    prop = Property("Prop", 1, 200, 20)
    
    # Can afford
    player.balance = 200
    with patch('builtins.input', return_value='y'):
        game.buy_property(player, prop)
    assert player.balance == 0
    assert prop.owner == player
    assert player.count_properties() == 1
    
    # Cannot afford
    prop2 = Property("Prop2", 2, 500, 50)
    with patch('builtins.print'):
        with patch('builtins.input', return_value='y'):
            game.buy_property(player, prop2)
    assert prop2.owner is None
    
def test_doubles_speeding():
    """Test that rolling 3 consecutive doubles sends player to jail."""
    game = Game(["P1", "P2"])
    player = game.players[0]
    
    # Provider 3 pairs of doubles for P1
    with patch('random.randint', side_effect=[1,1, 2,2, 3,3]):
        with patch('builtins.input', return_value='s'):
            # This causes loop in play_turn to strike 3 doubles
            game.play_turn()
            
    assert player.in_jail is True
    assert player.position == 10
