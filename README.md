# Comprehensive Testing Skills Showcase

A Python project demonstrating **advanced testing practices** and **test-driven development** through two well-tested domains: a banking system and an IP geolocation service. This repository showcases professional-level testing strategies, patterns, and tools used in production environments.

## 🧪 **Testing Skills Demonstrated**

### **Core Testing Practices**
- ✅ **Unit Testing** with pytest framework
- ✅ **Test Organization** using classes and logical grouping
- ✅ **Fixture Management** with shared and specialized fixtures
- ✅ **Mocking & Dependency Injection** for external services
- ✅ **Parametrized Testing** for comprehensive scenario coverage
- ✅ **Exception Testing** with proper error validation
- ✅ **Test Documentation** with clear docstrings and naming

### **Advanced Testing Techniques**
- ✅ **Coverage Reporting** with minimum 85% threshold enforcement
- ✅ **CI/CD Integration** with GitHub Actions
- ✅ **Test Data Generation** using faker library
- ✅ **Business Rule Testing** for domain-specific constraints
- ✅ **Edge Case Coverage** including boundary conditions
- ✅ **Repository Pattern Testing** with mock implementations

### **Testing Architecture**
- ✅ **Separation of Concerns** in test organization
- ✅ **Single Responsibility** per test method
- ✅ **Clean Test Code** following DRY principles
- ✅ **Maintainable Test Suites** with logical structure

## 🏗️ **Project Structure & Test Coverage**

### **Domain Modules (Testing Vehicles)**

#### Banking System Tests
```
tests/unit/banking/domain/
├── test_bank_account.py
└── test_user.py
```

#### Geolocation System Tests  
```
tests/unit/geolocation/
├── app/
│   └── test_geolocator.py   # API integration & error handling tests
└── domain/
    ├── test_geolocation.py  # Value object testing
    └── test_ip_address.py   # Input validation testing
```

## 🔧 **Testing Setup & Configuration**

### **Prerequisites**
- Python 3.8+
- pytest framework
- pytest-cov for coverage reporting

### **Installation**
```bash
git clone <repository-url>
cd python-testing
pip install -r requirements.txt
```

### **Running the Test Suite**

```bash
# Run all tests with coverage
pytest --cov=src --cov-report=html

# Run specific test modules
pytest tests/unit/banking/
pytest tests/unit/geolocation/

# Run with verbose output
pytest -v

# Run only failed tests from last run
pytest --lf

# Run specific test class
pytest tests/unit/banking/domain/test_bank_account.py::TestBankAccountCreation
```

## 📊 **Testing Metrics & Quality**

- **Coverage Threshold**: 85% minimum (enforced in CI/CD)
- **Test Count**: 50+ comprehensive test cases
- **Test Organization**: 8+ test classes with logical grouping
- **CI/CD Integration**: Automated testing on every push/PR

## 💡 **Key Testing Patterns Demonstrated**

### **1. Comprehensive Fixture Strategy**
```python
# Shared fixtures in conftest.py
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
```

### **2. Parametrized Testing for Multiple Scenarios**
```python
@pytest.mark.parametrize("deposit", [0, 50.50, 999999.99])
def test_should_increase_balance_when_depositing_positive_amount(self, empty_account, deposit):
    """Test depositing various positive amounts."""
    empty_account.deposit(deposit)
    assert empty_account.balance == deposit
```

### **3. Mock-Based External Dependency Testing**
```python
@pytest.fixture
def mock_repository():
    return Mock()

def test_get_location_when_repository_fails(geolocator, mock_repository):
    mock_repository.get_location_by_ip.side_effect = Exception("API Error")
    
    with pytest.raises(RepositoryError) as exc_info:
        geolocator.get_location("8.8.8.8")
    
    assert "API Error" in str(exc_info.value)
```

### **4. Business Rule & Edge Case Testing**
```python
def test_should_raise_error_when_withdrawing_outside_business_hours(self, funded_account):
    """Test withdrawal restrictions during non-business hours."""
    with patch('banking.domain.bank_account.datetime') as mock_datetime:
        mock_datetime.now.return_value = datetime(2023, 1, 1, 20, 0)  # 8 PM
        
        with pytest.raises(ValidationError) as exc_info:
            funded_account.withdraw(50)
        
        assert "Cannot perform operations outside business hours" in str(exc_info.value)
```

### **5. Exception Testing with Proper Validation**
```python
def test_should_raise_error_when_initial_balance_is_negative(self):
    """Test creating account with negative balance raises ValidationError."""
    with pytest.raises(ValidationError):
        BankAccount(balance=-100)
```

## 🎯 **Testing Best Practices Showcased**

### **Test Organization**
- **Class-based grouping** by functionality (Creation, Deposit, Withdrawal, etc.)
- **Descriptive test names** that explain the expected behavior
- **Comprehensive docstrings** for test documentation
- **Logical test file structure** mirroring source code organization

### **Test Quality**
- **Single responsibility** per test method
- **Arrange-Act-Assert** pattern consistently applied
- **No test interdependencies** - each test runs independently
- **Clear failure messages** with descriptive assertions

### **Coverage Strategy**
- **Positive and negative test cases** for all scenarios
- **Boundary condition testing** (zero values, limits, etc.)
- **Business rule enforcement** testing
- **Error path coverage** with proper exception handling

## 🔄 **Continuous Integration**

### **GitHub Actions Workflow**
- **Automated testing** on every push and pull request
- **Multi-step validation**: linting, testing, coverage reporting
- **Python 3.13** testing environment
- **Fail-fast approach** with immediate feedback

### **Quality Gates**
- **85% minimum coverage** requirement
- **All tests must pass** before merge
- **Code linting** with flake8
- **Automated dependency installation**

## 🛠️ **Dependencies & Tools**

```txt
pytest==8.0.0          # Testing framework
pytest-cov==4.0.0      # Coverage reporting  
faker==37.4.2           # Test data generation
requests==2.32.4        # HTTP library (for testing external APIs)
```

## 📈 **Learning Outcomes**

This project demonstrates proficiency in:

1. **Test Strategy Design** - Comprehensive test planning and execution
2. **Framework Mastery** - Advanced pytest features and plugins
3. **Mock Testing** - Proper isolation of units under test
4. **Coverage Analysis** - Understanding and achieving meaningful coverage
5. **CI/CD Integration** - Automated testing pipelines
6. **Test Maintenance** - Writing maintainable and scalable test suites
7. **Quality Assurance** - Implementing quality gates and standards

Perfect for showcasing **testing expertise** in technical interviews, code reviews, or portfolio demonstrations.

## 🚀 **Quick Test Demo**

```bash
# Clone and run the complete test suite
git clone <repository-url>
cd python-testing
pip install -r requirements.txt
pytest --cov=src --cov-report=term-missing -v
```

See comprehensive test output, coverage metrics, and quality indicators in action! 