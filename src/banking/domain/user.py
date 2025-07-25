from banking.domain.bank_account import BankAccount
from shared.exceptions.validation_error import ValidationError


class User:
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email
        self.__accounts = []

    @property
    def name(self) -> str:
        return self.__name

    @property
    def email(self) -> str:
        return self.__email

    @property
    def accounts(self) -> list[BankAccount]:
        return self.__accounts

    @name.setter
    def name(self, name: str) -> None:
        if not name or name.strip() == "":
            raise ValidationError("Name cannot be blank")
        self.__name = name
    
    @email.setter
    def email(self, email: str) -> None:
        if not email or email.strip() == "":
            raise ValidationError("Email cannot be blank")
        self.__email = email

    def add_account(self, account: BankAccount) -> None:
        if not isinstance(account, BankAccount):
            raise ValidationError("Account must be a BankAccount instance")
        
        self.__accounts.append(account)

    def total_balance(self) -> float:
        return sum(account.balance for account in self.__accounts)

    def __repr__(self) -> str:
        return f"User(name={self.__name}, email={self.__email}, accounts={self.__accounts})"