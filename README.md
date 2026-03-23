# DASS Assignment 2 Software Testing

## How to run the tests and the code

### Whitebox (MoneyPoly)
```bash
# To run the entire pytest suite boundary coverage:
pytest whitebox/tests/ -v

# To verify 10/10 code quality metrics:
cd whitebox/code && pylint moneypoly
```

### Integration (StreetRace Manager)
```bash
# To run the end-to-end integration mapping covering all 8 modules natively:
pytest integration/tests/test_integration.py -v
```

### Blackbox (QuickCart API)
```bash
# To unleash the 139 boundary fuzzing and structural API tests:
pytest blackbox/tests/ -v
```

## Git Repository Link
[https://github.com/Krypton711/DASS_A2](https://github.com/Krypton711/DASS_A2)
