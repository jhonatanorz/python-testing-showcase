import pytest
from faker import Faker

from banking.domain.user import User
from banking.domain.bank_account import BankAccount
from shared.exceptions.validation_error import ValidationError

fake = Faker()

@pytest.fixture
def user():
    """Create a user with faker-generated data."""
    return User(fake.name(), fake.email())


@pytest.fixture
def account_with_balance():
    """Create a bank account with random balance."""
    return BankAccount(fake.pyfloat(min_value=1.0, max_value=1000.0, right_digits=2))


class TestUserInitialization:
    """Test user creation."""

    def test_user_creation_with_blank_name_raises_error(self):
        """Test creating user with blank name raises ValidationError."""
        with pytest.raises(ValidationError, match="Name cannot be blank"):
            User("", fake.email())

    def test_user_creation_with_whitespace_only_name_raises_error(self):
        """Test creating user with whitespace-only name raises ValidationError."""
        with pytest.raises(ValidationError, match="Name cannot be blank"):
            User("   ", fake.email())

    def test_user_creation_with_blank_email_raises_error(self):
        """Test creating user with blank email raises ValidationError."""
        with pytest.raises(ValidationError, match="Email cannot be blank"):
            User(fake.name(), "")

    def test_user_creation_with_whitespace_only_email_raises_error(self):
        """Test creating user with whitespace-only email raises ValidationError."""
        with pytest.raises(ValidationError, match="Email cannot be blank"):
            User(fake.name(), "   ")

    def test_user_creation_initializes_empty_accounts(self, user):
        """Test that new user starts with empty accounts list."""
        assert user.accounts == []

    def test_user_creation_with_valid_data(self):
        """Test creating user with name and email."""
        name = fake.name()
        email = fake.email()
        user = User(name, email)
        
        assert user.name == name
        assert user.email == email


class TestUserNameProperty:
    """Test user name property."""

    def test_name_setter_with_blank_string_raises_error(self, user):
        """Test setting name to blank string raises ValidationError."""
        with pytest.raises(ValidationError, match="Name cannot be blank"):
            user.name = ""

    def test_name_setter_with_whitespace_only_raises_error(self, user):
        """Test setting name to whitespace-only string raises ValidationError."""
        with pytest.raises(ValidationError, match="Name cannot be blank"):
            user.name = "   "

    def test_name_getter(self, user):
        """Test getting name property returns correct value."""
        assert isinstance(user.name, str)
        assert len(user.name) > 0

    def test_name_setter_updates_value_correctly(self, user):
        """Test setting name property updates the value."""
        new_name = fake.name()
        user.name = new_name
        assert user.name == new_name


class TestUserEmailProperty:
    """Test user email property."""

    def test_email_setter_with_blank_string_raises_error(self, user):
        """Test setting email to blank string raises ValidationError."""
        with pytest.raises(ValidationError, match="Email cannot be blank"):
            user.email = ""

    def test_email_setter_with_whitespace_only_raises_error(self, user):
        """Test setting email to whitespace-only string raises ValidationError."""
        with pytest.raises(ValidationError, match="Email cannot be blank"):
            user.email = "   "

    def test_email_property_getter(self, user):
        """Test getting email property returns correct value."""
        assert isinstance(user.email, str)
        assert '@' in user.email

    def test_email_setter_updates_value_correctly(self, user):
        """Test setting email property updates the value."""
        new_email = fake.email()
        user.email = new_email
        assert user.email == new_email


class TestUserAccountsProperty:
    """Test user accounts property."""

    def test_accounts_property_getter_initially_empty(self, user):
        """Test that accounts property is initially empty."""
        assert user.accounts == []

    def test_accounts_property_getter_returns_list(self, user):
        """Test that accounts property returns a list."""
        assert isinstance(user.accounts, list)

    def test_accounts_property_getter_reflects_added_accounts(self, user, account_with_balance):
        """Test that accounts property shows added accounts."""
        user.add_account(account_with_balance)
        assert len(user.accounts) == 1
        assert user.accounts[0] is account_with_balance


class TestAddAccount:
    """Test adding accounts to user."""

    def test_add_not_account_raises_error(self, user, account_with_balance):
        """Test that adding the same account twice only adds it once."""
        with pytest.raises(ValidationError):
            user.add_account("not an account")

    def test_add_single_account(self, user, account_with_balance):
        """Test adding one account to user."""
        user.add_account(account_with_balance)
        
        assert len(user.accounts) == 1
        assert user.accounts[0] is account_with_balance

    def test_add_multiple_accounts(self, user):
        """Test adding multiple accounts to user."""
        accounts = [
            BankAccount(fake.pyfloat(min_value=0.0, max_value=1000.0, right_digits=2))
            for _ in range(3)
        ]
        
        for account in accounts:
            user.add_account(account)
        
        assert len(user.accounts) == 3
        for i, account in enumerate(accounts):
            assert user.accounts[i] is account


class TestCalculateTotalBalance:
    """Test user total balance calculation."""

    def test_total_balance_returns_zero_with_no_accounts(self, user):
        """Test total balance is zero when user has no accounts."""
        assert user.total_balance() == 0.0


    def test_total_balance_equals_single_account_balance(self, user):
        """Test total balance equals the single account balance."""
        balance = fake.pyfloat(min_value=1.0, max_value=1000.0, right_digits=2)
        account = BankAccount(balance)
        user.add_account(account)
        
        assert user.total_balance() == balance

    def test_total_balance_sums_multiple_account_balances(self, user):
        """Test total balance sums all account balances."""
        balances = [
            fake.pyfloat(min_value=0.0, max_value=1000.0, right_digits=2)
            for _ in range(3)
        ]
        expected_total = sum(balances)
        
        for balance in balances:
            user.add_account(BankAccount(balance))
        
        assert abs(user.total_balance() - expected_total) < 0.01
