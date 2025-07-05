# Test Organization

This directory contains the test suite for the project. The tests are organized following best practices for clarity, maintainability, and scalability.

## Directory Structure

```
tests/
├── conftest.py           # Shared fixtures and configuration
├── unit/                 # Unit tests directory
│   ├── test_bank_account.py  # Tests for BankAccount class
│   └── test_calculator.py    # Tests for Calculator class
└── README.md            # This file
```

## Test Categories

### Unit Tests (`unit/`)
Contains tests for individual components in isolation:
- `test_bank_account.py`: Tests for the BankAccount class operations
- `test_calculator.py`: Tests for the Calculator class operations

## Fixtures

Shared fixtures are defined in `conftest.py` and include:
- `empty_account`: Provides a new BankAccount instance with zero balance
- `funded_account`: Provides a BankAccount instance with 100 initial balance
- `calculator`: Provides a Calculator instance

## Test Organization Principles

1. **Test Grouping**: Tests are grouped by functionality into separate classes
2. **Naming Conventions**: 
   - Test files: `test_*.py`
   - Test classes: `Test*`
   - Test methods: `test_*`
3. **Documentation**: Each test class and method includes docstrings
4. **Single Responsibility**: Each test focuses on one specific behavior
5. **Independence**: Tests are independent and can run in any order

## Running Tests

To run all tests:
```bash
python -m pytest
```

To run specific test categories:
```bash
python -m pytest tests/unit/  # Run all unit tests
python -m pytest tests/unit/test_bank_account.py  # Run bank account tests only
``` 