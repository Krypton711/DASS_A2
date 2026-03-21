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
| `test_give_loan_reduces_funds` | Bank issues a loan | `amount` > 0 | Validates control flow of `give_loan`. | `self._funds` didn't decrease when issuing loans. |
| `test_payout_insufficient_funds` | Bank pays out more than reserves | `amount` > `self._funds` | Validates boundary check array. | None |
| `test_negative_payout_and_loan` | Zero or negative amounts | `amount` <= 0 | Validates early returns on Edge Cases. | None |
| `test_collect_funds` | Bank collects funds | `amount` > 0 | Validates basic inflow. | None |

### Corrected Errors (Commits)
- Error 1: Fixed `give_loan` in `bank.py` not deducting from bank reserves.
- Error 2: <What You Changed>
