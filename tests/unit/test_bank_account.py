"""Unit tests for the BankAccount class."""

import pytest
from src.bank_account import BankAccount


class TestBankAccountDeposit:
    """Test cases for BankAccount deposit operations."""

    def test_should_raise_error_when_depositing_negative_amount(self, empty_account):
        """Test depositing a negative amount raises ValueError."""
        with pytest.raises(ValueError):
            empty_account.deposit(-50)

    def test_should_maintain_balance_when_depositing_zero(self, empty_account):
        """Test depositing zero amount does not change the balance."""
        initial_balance = empty_account.balance
        empty_account.deposit(0)
        assert empty_account.balance == initial_balance, "Depositing zero should not change the balance"

    def test_should_have_zero_balance_when_account_is_created(self, empty_account):
        """Test initial balance of the account."""
        assert empty_account.balance == 0, "Initial balance should be zero"

    def test_should_increase_balance_when_depositing_positive_amount(self, empty_account):
        """Test depositing a positive amount."""
        empty_account.deposit(100)
        assert empty_account.balance == 100, "Failed to deposit positive amount correctly"


class TestBankAccountWithdraw:
    """Test cases for BankAccount withdraw operations."""

    def test_should_raise_error_when_withdrawing_negative_amount(self, funded_account):
        """Test withdrawing a negative amount raises ValueError."""
        with pytest.raises(ValueError):
            funded_account.withdraw(-50)
    
    def test_should_raise_error_when_withdrawal_exceeds_balance(self, empty_account):
        """Test withdrawing an amount that exceeds the balance raises ValueError."""
        with pytest.raises(ValueError):
            empty_account.withdraw(100)

    def test_should_maintain_balance_when_withdrawing_zero(self, funded_account):
        """Test withdrawing zero amount does not change the balance."""
        initial_balance = funded_account.balance
        funded_account.withdraw(0)
        assert funded_account.balance == initial_balance, "Withdrawing zero should not change the balance"

    def test_should_decrease_balance_when_withdrawing_valid_amount(self, funded_account):
        """Test withdrawing a positive amount."""
        funded_account.withdraw(50)
        assert funded_account.balance == 50, "Failed to withdraw positive amount correctly"

    def test_should_set_balance_to_zero_when_withdrawing_entire_amount(self, funded_account):
        """Test withdrawing the entire balance."""
        funded_account.withdraw(100)
        assert funded_account.balance == 0, "Withdrawing entire balance should leave zero"


class TestBankAccountTransfers:
    """Test cases for BankAccount transfer operations."""

    def test_should_raise_error_when_transfer_amount_is_negative(self, funded_account, empty_account):
        """Test transferring a negative amount raises ValueError."""
        with pytest.raises(ValueError):
            funded_account.transfer(-50, empty_account)

    def test_should_raise_error_when_transfer_exceeds_balance(self, empty_account):
        """Test transferring an amount that exceeds the balance raises ValueError."""
        destination = BankAccount()
        with pytest.raises(ValueError):
            empty_account.transfer(100, destination)

    def test_should_raise_error_when_destination_account_is_none(self, funded_account):
        """Test transferring to None raises ValueError."""
        with pytest.raises(ValueError):
            funded_account.transfer(50, None)

    def test_should_raise_error_when_transferring_to_same_account(self, funded_account):
        """Test transferring to the same account raises ValueError."""
        with pytest.raises(ValueError):
            funded_account.transfer(50, funded_account)

    def test_should_raise_error_when_destination_is_invalid_type(self, funded_account):
        """Test transferring to non-BankAccount object raises ValueError."""
        with pytest.raises(ValueError):
            funded_account.transfer(50, {"balance": 100})

    def test_should_maintain_balances_when_transfer_amount_is_zero(self, funded_account, empty_account):
        """Test transferring zero amount does not change either balance."""
        initial_source_balance = funded_account.balance
        initial_dest_balance = empty_account.balance
        
        funded_account.transfer(0, empty_account)
        
        assert funded_account.balance == initial_source_balance, "Source balance changed"
        assert empty_account.balance == initial_dest_balance, "Destination balance changed"

    def test_should_update_both_balances_when_transfer_is_valid(self, funded_account, empty_account):
        """Test transferring a positive amount between accounts."""
        funded_account.transfer(50, empty_account)
        assert funded_account.balance == 50, "Source account balance incorrect after transfer"
        assert empty_account.balance == 50, "Destination account balance incorrect after transfer"

    def test_should_transfer_all_funds_when_amount_equals_balance(self, funded_account, empty_account):
        """Test transferring the entire balance works correctly."""
        funded_account.transfer(100, empty_account)
        assert funded_account.balance == 0, "Source account should have zero balance"
        assert empty_account.balance == 100, "Destination should receive full amount"


class TestBankAccountDeactivation:

    @pytest.mark.skip(reason="Not implemented")
    def test_should_mark_account_inactive_when_deactivation_is_requested(self, funded_account):
        """Test deactivating an active account."""
        funded_account.deactivate()
        assert funded_account.active == False, "Account should be inactive after deactivation"