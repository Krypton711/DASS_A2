import pytest
from unittest.mock import patch
from moneypoly.dice import Dice

def test_dice_rolls_valid_range():
    """Test that dice faces simulate 1-6."""
    dice = Dice()
    for _ in range(100):
        total = dice.roll()
        assert 1 <= dice.die1 <= 6
        assert 1 <= dice.die2 <= 6
        assert 2 <= total <= 12

def test_doubles_streak():
    """Test that doubles streak increments on doubles and resets on non-doubles."""
    dice = Dice()
    
    with patch('random.randint', side_effect=[3, 3]):
        dice.roll()
    assert dice.doubles_streak == 1
    assert dice.is_doubles() is True

    with patch('random.randint', side_effect=[4, 4]):
        dice.roll()
    assert dice.doubles_streak == 2
    
    with patch('random.randint', side_effect=[2, 5]):
        dice.roll()
    assert dice.doubles_streak == 0
    assert dice.is_doubles() is False

def test_dice_describe():
    """Test string description."""
    dice = Dice()
    with patch('random.randint', side_effect=[2, 3]):
        dice.roll()
    assert dice.describe() == "2 + 3 = 5"
    
    with patch('random.randint', side_effect=[4, 4]):
        dice.roll()
    assert dice.describe() == "4 + 4 = 8 (DOUBLES)"
