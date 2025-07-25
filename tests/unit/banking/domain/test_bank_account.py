import pytest

from unittest.mock import patch
from datetime import datetime

from banking.domain.bank_account import BankAccount
from shared.exceptions.validation_error import ValidationError


class TestBankAccountCreation:
    """Test cases for BankAccount creation and initialization."""

    def test_should_raise_error_when_initial_balance_is_negative(self):
        """Test creating a bank account with negative initial balance raises ValidationError."""
        with pytest.raises(ValidationError):
            BankAccount(balance=-100)

    def test_should_initialize_with_zero_balance_by_default(self):
        """Test that a new bank account has an initial balance of zero."""
        account = BankAccount()
        assert account.balance == 0, "New account should have zero balance by default"

    def test_should_initialize_with_positive_balance(self):
        """Test that a new bank account can be initialized with a positive balance."""
        account = BankAccount(balance=100)
        assert account.balance == 100, "New account should have the specified positive balance"

class TestBankAccountDeposit:
    """Test cases for BankAccount deposit operations."""

    def test_should_raise_error_when_depositing_negative_amount(self, empty_account):
        """Test depositing a negative amount raises ValidationError."""
        with pytest.raises(ValidationError):
            empty_account.deposit(-50)

    def test_should_maintain_balance_when_depositing_zero(self, empty_account):
        """Test depositing zero amount does not change the balance."""
        initial_balance = empty_account.balance
        empty_account.deposit(0)
        assert empty_account.balance == initial_balance, "Depositing zero should not change the balance"

    def test_should_have_zero_balance_when_account_is_created(self, empty_account):
        """Test initial balance of the account."""
        assert empty_account.balance == 0, "Initial balance should be zero"

    @pytest.mark.parametrize("deposit", [0, 50.50, 999999.99])
    def test_should_increase_balance_when_depositing_positive_amount(self, empty_account, deposit):
        """Test depositing a positive amount."""
        empty_account.deposit(deposit)
        assert empty_account.balance == deposit, "Failed to deposit positive amount correctly"


class TestBankAccountWithdraw:
    """Test cases for BankAccount withdraw operations."""

    def test_should_raise_error_when_account_is_deactivated(self, inactive_account):
        """Test withdrawing when account is deactivated raises ValidationError."""
        with pytest.raises(ValidationError):
            inactive_account.withdraw(100)

    def test_should_raise_error_when_withdrawing_negative_amount(self, funded_account):
        """Test withdrawing a negative amount raises ValidationError."""
        with pytest.raises(ValidationError):
            funded_account.withdraw(-50)
    
    def test_should_raise_error_when_withdrawal_exceeds_balance(self, empty_account):
        """Test withdrawing an amount that exceeds the balance raises ValidationError."""
        with pytest.raises(ValidationError):
            empty_account.withdraw(100)

    @patch('banking.domain.bank_account.datetime')
    def test_should_raise_error_when_withdrawing_outside_business_hours(self, mock_datetime, funded_account):
        """Test withdrawing outside business hours raises WithdrawalOutsideBusinessHoursError."""
        
        mock_datetime.now.return_value = datetime(2025, month=7, day=8, hour=20)
        
        with pytest.raises(ValidationError):
            funded_account.withdraw(50)

    @patch('banking.domain.bank_account.datetime')
    def test_should_raise_error_when_withdrawing_on_saturday(self, mock_datetime, funded_account):
        """Test withdrawing outside business hours raises WithdrawalOutsideBusinessHoursError."""
        
        mock_datetime.now.return_value = datetime(2025, month=7, day=12, hour=12)  # Saturday
        
        with pytest.raises(ValidationError):
            funded_account.withdraw(50)

    @patch('banking.domain.bank_account.datetime')
    def test_should_raise_error_when_withdrawing_on_sunday(self, mock_datetime, funded_account):
        """Test withdrawing outside business hours raises WithdrawalOutsideBusinessHoursError."""
        from datetime import datetime
        
        mock_datetime.now.return_value = datetime(2025, month=7, day=13, hour=12)  # Sunday
        
        with pytest.raises(ValidationError):
            funded_account.withdraw(50)

    @patch('banking.domain.bank_account.datetime')
    def test_should_maintain_balance_when_withdrawing_zero(self, mock_datetime, funded_account):
        """Test withdrawing zero amount does not change the balance."""
        from datetime import datetime
        initial_balance = funded_account.balance

        mock_datetime.now.return_value = datetime(2024, month=7, day=8, hour=12)

        funded_account.withdraw(0)
        assert funded_account.balance == initial_balance, "Withdrawing zero should not change the balance"

    @patch('banking.domain.bank_account.datetime')
    def test_should_decrease_balance_when_withdrawing_valid_amount(self, mock_datetime, funded_account):
        """Test withdrawing a positive amount."""
        from datetime import datetime
        
        mock_datetime.now.return_value = datetime(2024, month=7, day=8, hour=12)

        funded_account.withdraw(50)
        assert funded_account.balance == 50, "Failed to withdraw positive amount correctly"

    @patch('banking.domain.bank_account.datetime')
    def test_should_set_balance_to_zero_when_withdrawing_entire_amount(self, mock_datetime, funded_account):
        """Test withdrawing the entire balance."""
        from datetime import datetime
        
        mock_datetime.now.return_value = datetime(2024, month=7, day=8, hour=12)

        funded_account.withdraw(100)
        assert funded_account.balance == 0, "Withdrawing entire balance should leave zero"


class TestBankAccountTransfers:
    """Test cases for BankAccount transfer operations."""

    def test_should_raise_error_when_transfer_amount_is_negative(self, funded_account, empty_account):
        """Test transferring a negative amount raises ValidationError."""
        with pytest.raises(ValidationError):
            funded_account.transfer(-50, empty_account)

    def test_should_raise_error_when_transfer_exceeds_balance(self, empty_account):
        """Test transferring an amount that exceeds the balance raises ValidationError."""
        destination = BankAccount()
        with pytest.raises(ValidationError):
            empty_account.transfer(100, destination)

    def test_should_raise_error_when_destination_account_is_none(self, funded_account):
        """Test transferring to None raises ValidationError."""
        with pytest.raises(ValidationError):
            funded_account.transfer(50, None)

    def test_should_raise_error_when_transferring_to_same_account(self, funded_account):
        """Test transferring to the same account raises ValidationError."""
        with pytest.raises(ValidationError):
            funded_account.transfer(50, funded_account)

    def test_should_raise_error_when_destination_is_invalid_type(self, funded_account):
        """Test transferring to non-BankAccount object raises ValidationError."""
        with pytest.raises(ValidationError):
            funded_account.transfer(50, {"balance": 100})

    @patch('banking.domain.bank_account.datetime')
    def test_should_maintain_balances_when_transfer_amount_is_zero(self, mock_datetime, funded_account, empty_account):
        """Test transferring zero amount does not change either balance."""
        
        from datetime import datetime
        
        mock_datetime.now.return_value = datetime(2024, month=7, day=8, hour=12)
        
        initial_source_balance = funded_account.balance
        initial_dest_balance = empty_account.balance
        
        funded_account.transfer(0, empty_account)
        
        assert funded_account.balance == initial_source_balance, "Source balance changed"
        assert empty_account.balance == initial_dest_balance, "Destination balance changed"

    @patch('banking.domain.bank_account.datetime')
    def test_should_update_both_balances_when_transfer_is_valid(self, mock_datetime, funded_account, empty_account):
        """Test transferring a positive amount between accounts."""
        from datetime import datetime
        
        mock_datetime.now.return_value = datetime(2024, month=7, day=8, hour=12)
        
        funded_account.transfer(50, empty_account)
        assert funded_account.balance == 50, "Source account balance incorrect after transfer"
        assert empty_account.balance == 50, "Destination account balance incorrect after transfer"

    @patch('banking.domain.bank_account.datetime')
    def test_should_transfer_all_funds_when_amount_equals_balance(self, mock_datetime, funded_account, empty_account):
        """Test transferring the entire balance works correctly."""
        from datetime import datetime
        
        mock_datetime.now.return_value = datetime(2024, month=7, day=8, hour=12)
        
        funded_account.transfer(100, empty_account)
        assert funded_account.balance == 0, "Source account should have zero balance"
        assert empty_account.balance == 100, "Destination should receive full amount"


class TestBankAccountDeactivation:

    def test_should_mark_account_inactive_when_deactivation_is_requested(self, empty_account):
        """Test deactivating an active account."""
        empty_account.deactivate()
        assert empty_account.active == False, "Account should be inactive after deactivation"