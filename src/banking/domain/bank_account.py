from dataclasses import dataclass
from datetime import datetime
from typing import Union

from shared.exceptions.validation_error import ValidationError

Number = Union[int, float]

@dataclass
class BankAccount:
    """Entity representing a bank account."""
    
    def __init__(self, balance: Number = 0):
        """Initialize the bank account with an initial balance."""
        if balance < 0:
            raise ValidationError("Initial balance cannot be negative")
        self.__balance = balance
        self.__active = True
        
    @property
    def balance(self) -> Number:
        """Get the current balance of the account."""
        return self.__balance

    @property
    def active(self) -> bool:
        """Get the active status of the account."""
        return self.__active
    
    def deposit(self, amount: Number) -> None:
        """Deposit an amount into the account.
        
        Args:
            amount: The amount to deposit, must be positive.
            
        Raises:
            ValidationError: If the amount is negative.
            ValidationError: If the account is deactivated.
        """
        self._validate_active()
        self._validate_amount(amount)
        self.__balance += amount

    def withdraw(self, amount: Number) -> None:
        """Withdraw an amount from the account.
        
        Args:
            amount: The amount to withdraw, must be positive.
            
        Raises:
            ValidationError: If the amount is negative or exceeds the balance.
            ValidationError: If the account is deactivated.
            WithdrawalOutsideBusinessHoursError: If current time is not within business hours.
        """
        self._validate_active()
        self._validate_amount(amount)
        self._validate_sufficient_balance(amount)
        self._validate_within_withdrawal_time()
        self.__balance -= amount

    def transfer(self, amount: Number, other_account: 'BankAccount') -> None:
        """Transfer an amount to another account.
        
        Args:
            amount: The amount to transfer, must be positive.
            other_account: The account to transfer the amount to.
            
        Raises:
            ValidationError: If the amount is negative or exceeds the balance.
            ValidationError: If the other account is not a BankAccount.
            ValidationError: If attempting to transfer to the same account.
            ValidationError: If either account is deactivated.
        """
        self._validate_active()
        if not isinstance(other_account, BankAccount):
            raise ValidationError("Destination must be a BankAccount instance")
        
        if other_account is self:
            raise ValidationError("Cannot transfer to the same account")
            
        if not other_account.active:
            raise ValidationError("Cannot transfer to a deactivated account")
            
        self._validate_amount(amount)
        self._validate_sufficient_balance(amount)
            
        self.withdraw(amount)
        other_account.deposit(amount)

    def deactivate(self) -> None:
        """Deactivate the account.
        
        Raises:
            ValidationError: If the account is already deactivated.
            ValidationError: If the account has remaining balance.
        """
        if not self.__active:
            raise ValidationError("Account is already deactivated")
        
        if self.__balance > 0:
            raise ValidationError("Cannot deactivate account with remaining balance")
            
        self.__active = False

    def _validate_within_withdrawal_time(self) -> None:
        """Validate that current time is within business hours.
        
        Raises:
            ValidationError: If current time is not within business hours.
        """
        now = datetime.now()

        # Check if the current day is a weekend. 0 is Monday, 6 is Sunday.
        if now.weekday() > 4:
            raise ValidationError("Cannot perform operations outside business days")

        if now.hour < 9 or now.hour > 17:
            raise ValidationError("Cannot perform operations outside business hours")
        
    def _validate_active(self) -> None:
        """Validate that the account is active.
        
        Raises:
            ValidationError: If the account is deactivated.
        """
        if not self.__active:
            raise ValidationError("Account is deactivated")
            
    def _validate_amount(self, amount: Number) -> None:
        """Validate that an amount is positive.
        
        Args:
            amount: The amount to validate
            
        Raises:
            ValidationError: If the amount is negative.
        """
        if amount < 0:
            raise ValidationError("Amount must be positive")
            
    def _validate_sufficient_balance(self, amount: Number) -> None:
        """Validate that the account has sufficient balance.
        
        Args:
            amount: The amount to validate
            
        Raises:
            ValidationError: If the amount exceeds the balance.
        """
        if amount > self.__balance:
            raise ValidationError("Insufficient balance") 