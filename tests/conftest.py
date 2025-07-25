"""Shared fixtures and configuration for all tests."""

import pytest
from banking.domain.bank_account import BankAccount


@pytest.fixture
def empty_account():
    """Fixture providing a new empty bank account."""
    return BankAccount()


@pytest.fixture
def funded_account():
    """Fixture providing a bank account with initial funds."""
    account = BankAccount()
    account.deposit(100)
    return account 

@pytest.fixture
def inactive_account():
    """Fixture providing a bank account that is deactivated."""
    account = BankAccount()
    account.deactivate()
    return account