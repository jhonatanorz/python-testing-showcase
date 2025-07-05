from typing import Union

Number = Union[int, float]

class BankAccount:
    
    def __init__(self, balance: Number = 0):
        """Initialize the bank account with an initial balance."""
        self.__balance = balance
        self.__active = True
        
    @property
    def balance(self):
        """Get the current balance of the account."""
        return self.__balance

    @property
    def active(self):
        """Get the active status of the account."""
        return self.__active
    
    def deposit(self, amount : Number):
        """Deposit an amount into the account.
        
        Args:
            amount: The amount to deposit, must be positive.
            
        Raises:
            ValueError: If the amount is negative.
        """
        if amount < 0:
            raise ValueError("Amount must be positive")
        self.__balance += amount

    def withdraw(self, amount: Number):
        """Withdraw an amount from the account.
        
        Args:
            amount: The amount to withdraw, must be positive.
            
        Raises:
            ValueError: If the amount is negative or exceeds the balance.
        """
        if amount < 0:
            raise ValueError("Amount must be positive")
        if amount > self.__balance:
            raise ValueError("Insufficient balance")
        self.__balance -= amount

    def transfer(self, amount: Number, other_account: 'BankAccount') -> None:
        """Transfer an amount to another account.
        
        Args:
            amount: The amount to transfer, must be positive.
            other_account: The account to transfer the amount to.
            
        Raises:
            ValueError: If the amount is negative or exceeds the balance.
            ValueError: If the other account is not a BankAccount.
            ValueError: If attempting to transfer to the same account.
            ValueError: If the other_account is None.
        """
        if not isinstance(other_account, BankAccount):
            raise ValueError("Destination must be a BankAccount instance")
        
        if other_account is self:
            raise ValueError("Cannot transfer to the same account")
            
        if amount < 0:
            raise ValueError("Amount must be positive")
            
        if amount > self.balance:
            raise ValueError("Insufficient balance")
            
        self.withdraw(amount)
        other_account.deposit(amount)

    def deactivate(self):
        """Deactivate the account.
        
        Raises:
            ValueError: If the account is already deactivated.
        """
        pass