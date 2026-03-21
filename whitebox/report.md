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
| `test_dice_rolls_valid_range` | Roll dice 100 times | Iterative large input | Checks if face values conform to 6-sided dice logic. | The dice were rolling `randint(1, 5)` instead of 1 to 6! |
| `test_doubles_streak` | Roll consecutive doubles then non-double | Doubles branch logic | Covers `is_doubles()` true and false branches and streak reset. | None |
| `test_dice_describe` | Describe rolls with/without doubles | String formatting | Covers the conditional branch in the describe string. | None |
| `test_property_rent_calculation` | Mixed ownership vs Full ownership | `group.all_owned_by` branch | Verifies rent doubling logic and mortgage rent logic. | `all_owned_by` was using `any()` instead of `all()`, making single ownership trigger double rent! |
| `test_property_mortgage_unmortgage` | Double mortgage/unmortgage | `is_mortgaged` state | Verifies early returns and correct cost calculations. | None |
| `test_property_is_available` | Check unowned, owned, and mortgaged | `owner` and `is_mortgaged` states | Covers all combinations of availability checks. | None |
| `test_player_money_management` | Add/deduct negative/positive | `amount` edge cases | Tests ValueError for negative values and `is_bankrupt` logic. | None |
| `test_player_movement_and_go` | Move across GO threshold | `position` wrap-around | Tests whether passing GO awards the salary correctly. | Found that `move` only awarded salary on exactly 0, not when passing GO! |
| `test_player_properties` | Duplicate add/remove | `properties` list state | Ensures list operations handle existing/missing items safely. | None |

### Corrected Errors (Commits)
- Error 1: Fixed `give_loan` in `bank.py` not deducting from bank reserves.
- Error 2: Fixed `dice.py` rolling 1 to 5 instead of 1 to 6 for six-sided dice.
- Error 3: Fixed `PropertyGroup.all_owned_by` in `property.py` using `any()` instead of `all()`.
- Error 4: Fixed `player.move` to award GO_SALARY when passing GO, not just landing exactly on it.
