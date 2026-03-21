# White Box Testing Report

## 1.1 Control Flow Graph
<!-- Attach hand-drawn Control Flow Graph image here -->

## 1.2 Code Quality Analysis
### Pylint Iterations
| Iteration | Changes Made |
| :--- | :--- |
| Iteration 1: Fix unused vars and imports | Removed unused imports (sys, os, math, etc) and `old_position` variable. |
| Iteration 2: Add missing docstrings | Added module docstrings to 9 files and class docstrings to Bank, PropertyGroup. |
| Iteration 3: Formatting and syntax | Added trailing newlines to player.py and game.py. Removed unnecessary parens in game.py and reformatted dictionaries in cards.py to avoid long lines. |
| Iteration 4: Logical and best practices | Replaced bare except in ui.py, fixed truthiness comparison in board.py, removed unnecessary else in property.py, fixed redundant f-string and elif in game.py. |
| Iteration 5: Refactoring | Fixed W0201 by moving `doubles_streak` inside `__init__` in `dice.py`. Fixed `too-many-instance-attributes (R0902)` by grouping attributes into a `_state` dict in `player.py`, replacing `mortgage_value` with a `@property` in `property.py`, and combining decks into a `decks` dict in `game.py`. Replaced long if/elif branch structure with a method dispatch table in `game.py` to fix `too-many-branches`. |

## 1.3 White Box Test Cases

### Test Cases Justification
| Test Case | Scenario | Variables/Edge Cases | Reason for Inclusion | Errors/Issues Found |
| :--- | :--- | :--- | :--- | :--- |
| 1 | | | | |
| 2 | | | | |

### Corrected Errors (Commits)
- Error 1: <What You Changed>
- Error 2: <What You Changed>
