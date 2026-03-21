import pytest
from unittest.mock import patch
import moneypoly.ui as ui
from moneypoly.game import Game
from moneypoly.property import Property

def test_ui_safe_int_input_eof():
    """Test safe_int_input handles non-integer and EOF inputs gracefully."""
    with patch('builtins.input', side_effect=EOFError):
        assert ui.safe_int_input("test", 99) == 99

def test_auction_non_integer_bid():
    """Test that auction does not crash when encountering non-integer input."""
    game = Game(["P1", "P2"])
    prop = Property("Prop", 1, 200, 20)
    
    # P1 bids 5, P2 bids 10, P1 bids "five" (returns 0 natively) and drops out.
    with patch('builtins.input', side_effect=["5", "10", "five"]):
        game.auction_property(prop)
        
    assert prop.owner == game.players[1]
    assert game.players[1].balance == 1490

def test_trade_negative_cash():
    """Test that trading for negative cash is aborted properly."""
    game = Game(["P1", "P2"])
    p1 = game.players[0]
    prop = Property("Prop", 1, 200, 20)
    prop.owner = p1
    p1.add_property(prop)
    
    # 1 to select P2, 1 to select Prop, -50 to request negative cash.
    # It should print "Cash amount cannot be negative" and abort.
    with patch('builtins.input', side_effect=["1", "1", "-50"]):
        with patch('builtins.print') as mock_print:
            game._menu_trade(p1)
            
    mock_print.assert_any_call("  Cash amount cannot be negative.")
    # Check that money wasn't exchanged
    assert game.players[0].balance == 1500
    assert game.players[1].balance == 1500
