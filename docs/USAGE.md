# Usage Guide

Comprehensive guide for using the Selenium PyTest Framework effectively.

---

## Table of Contents

1. [Writing Tests](#writing-tests)
2. [Creating Page Objects](#creating-page-objects)
3. [Using Fixtures](#using-fixtures)
4. [Data-Driven Testing](#data-driven-testing)
5. [Reporting](#reporting)
6. [Best Practices](#best-practices)
7. [Advanced Features](#advanced-features)

---

## Writing Tests

### Basic Test Structure

```python
import pytest
from pages.login_page import LoginPage

@pytest.mark.smoke
def test_login(driver):
    """Test user login functionality"""
    login_page = LoginPage(driver)
    
    # Navigate to page
    login_page.navigate()
    
    # Perform actions
    login_page.login("username", "password")
    
    # Assertions
    assert login_page.is_login_successful()
```

### Test Class Structure

```python
@pytest.mark.regression
class TestLoginFeature:
    """Test suite for login feature"""
    
    def test_valid_login(self, driver):
        """Test with valid credentials"""
        # Test implementation
        pass
    
    def test_invalid_login(self, driver):
        """Test with invalid credentials"""
        # Test implementation
        pass
```

### Using Test Markers

```python
@pytest.mark.smoke          # Quick smoke test
@pytest.mark.regression     # Full regression
@pytest.mark.critical       # Critical path
@pytest.mark.slow           # Slow-running test
@pytest.mark.skip_in_ci     # Skip in CI/CD

# Multiple markers
@pytest.mark.smoke
@pytest.mark.critical
def test_important_feature(driver):
    pass
```

---

## Creating Page Objects

### Page Object Template

```python
from selenium.webdriver.common.by import By
from core.base_page import BasePage
from utils.logger import logger

class YourPage(BasePage):
    """Page object for Your Page"""
    
    # Locators
    ELEMENT_ONE = (By.ID, "element-id")
    ELEMENT_TWO = (By.CSS_SELECTOR, ".class-name")
    BUTTON = (By.XPATH, "//button[@name='submit']")
    
    def __init__(self, driver):
        super().__init__(driver)
        self.url = "https://example.com/your-page"
    
    def navigate(self):
        """Navigate to this page"""
        logger.info(f"Navigating to {self.url}")
        self.navigate_to(self.url)
        return self
    
    def is_displayed(self) -> bool:
        """Check if page is displayed"""
        return self.is_element_visible(self.ELEMENT_ONE)
    
    def perform_action(self, value: str):
        """Perform specific action"""
        logger.info(f"Performing action with value: {value}")
        self.type_text(self.ELEMENT_ONE, value)
        self.click(self.BUTTON)
        return self
    
    def get_result(self) -> str:
        """Get result from page"""
        return self.get_text(self.ELEMENT_TWO)
```

### Locator Strategies

```python
# ID (Preferred - fastest and most reliable)
ELEMENT = (By.ID, "element-id")

# CSS Selector (Fast and flexible)
ELEMENT = (By.CSS_SELECTOR, ".class-name")
ELEMENT = (By.CSS_SELECTOR, "#id-name")
ELEMENT = (By.CSS_SELECTOR, "[data-test='value']")

# XPATH (Powerful but slower)
ELEMENT = (By.XPATH, "//div[@class='name']")
ELEMENT = (By.XPATH, "//button[text()='Click Me']")

# Other strategies
ELEMENT = (By.NAME, "element-name")
ELEMENT = (By.CLASS_NAME, "class-name")
ELEMENT = (By.LINK_TEXT, "Link Text")
ELEMENT = (By.PARTIAL_LINK_TEXT, "Partial")
ELEMENT = (By.TAG_NAME, "div")
```

### Page Object Methods

```python
# Navigation
self.navigate_to(url)
self.refresh_page()
self.go_back()

# Element Interactions
self.click(locator)
self.type_text(locator, text)
self.get_text(locator)
self.get_attribute(locator, "attribute")
self.clear_field(locator)

# Advanced Interactions
self.hover_over_element(locator)
self.double_click_element(locator)
self.right_click_element(locator)
self.drag_and_drop(source, target)

# Waits
self.wait_for_element_visible(locator)
self.wait_for_element_invisible(locator)
self.is_element_present(locator)
self.is_element_visible(locator)

# JavaScript
self.execute_script(script)
self.scroll_to_element(locator)
self.click_with_js(locator)

# Frames and Windows
self.switch_to_frame(locator)
self.switch_to_default_content()
self.switch_to_window(handle)
```

---

## Using Fixtures

### Available Fixtures

```python
def test_with_driver(driver):
    """Basic driver fixture"""
    driver.get("https://example.com")

def test_with_logged_in_driver(logged_in_driver):
    """Pre-logged-in driver"""
    # User is already logged in
    pass

def test_with_test_users(test_users):
    """Access test user credentials"""
    user = test_users["standard_user"]
    username = user["username"]

def test_with_base_url(base_url):
    """Access base URL"""
    print(f"Testing against: {base_url}")
```

### Creating Custom Fixtures

```python
# In conftest.py
@pytest.fixture
def sample_data():
    """Provide sample test data"""
    return {
        "name": "John Doe",
        "email": "john@example.com"
    }

@pytest.fixture(scope="class")
def database_connection():
    """Setup database connection"""
    conn = create_connection()
    yield conn
    conn.close()

# Using the fixture
def test_with_sample_data(driver, sample_data):
    page = RegistrationPage(driver)
    page.fill_form(sample_data)
```

---

## Data-Driven Testing

### Using Parametrize

```python
@pytest.mark.parametrize("username,password,expected", [
    ("valid_user", "valid_pass", True),
    ("invalid_user", "wrong_pass", False),
    ("", "password", False),
    ("username", "", False)
])
def test_login_scenarios(driver, username, password, expected):
    login_page = LoginPage(driver)
    login_page.navigate()
    login_page.login(username, password)
    
    if expected:
        assert login_page.is_login_successful()
    else:
        assert login_page.is_error_displayed()
```

### Using JSON Data

```python
# test_data/users.json
{
    "valid_users": [
        {"username": "user1", "password": "pass1"},
        {"username": "user2", "password": "pass2"}
    ]
}

# In test
import json

def load_test_data():
    with open('test_data/users.json') as f:
        return json.load(f)

@pytest.mark.parametrize("user", load_test_data()["valid_users"])
def test_with_json_data(driver, user):
    login_page = LoginPage(driver)
    login_page.login(user["username"], user["password"])
```

---

## Reporting

### HTML Reports

```bash
# Generate HTML report
pytest --html=reports/report.html --self-contained-html

# With custom CSS
pytest --html=reports/report.html --css=custom.css
```

### Allure Reports

```bash
# Install Allure
pip install allure-pytest

# Generate Allure results
pytest --alluredir=reports/allure

# Serve Allure report
allure serve reports/allure

# Generate static report
allure generate reports/allure -o reports/allure-report --clean
```

### Adding Allure Annotations

```python
import allure

@allure.feature('Login')
@allure.story('User Authentication')
@allure.title('Test successful login')
@allure.description('Verify user can login with valid credentials')
@allure.severity(allure.severity_level.CRITICAL)
def test_login(driver):
    with allure.step('Navigate to login page'):
        login_page = LoginPage(driver)
        login_page.navigate()
    
    with allure.step('Enter credentials'):
        login_page.login("user", "pass")
    
    with allure.step('Verify login success'):
        assert login_page.is_login_successful()
```

---

## Best Practices

### 1. Test Independence

```python
# ❌ Bad - Tests depend on each other
def test_create_user(driver):
    # Creates user
    pass

def test_login_user(driver):
    # Assumes user from previous test exists
    pass

# ✅ Good - Each test is independent
def test_create_user(driver):
    # Setup + Test + Cleanup
    pass

def test_login_user(driver, test_users):
    # Uses fixture for known user
    pass
```

### 2. Clear Test Names

```python
# ❌ Bad
def test_1(driver):
    pass

# ✅ Good
def test_user_can_login_with_valid_credentials(driver):
    pass

def test_error_displayed_for_invalid_password(driver):
    pass
```

### 3. One Assertion Per Concept

```python
# ❌ Bad - Multiple unrelated assertions
def test_page(driver):
    assert element1.is_displayed()
    assert element2.text == "value"
    assert button.is_enabled()

# ✅ Good - Related assertions grouped
def test_page_elements_displayed(driver):
    assert element1.is_displayed()
    assert element2.is_displayed()

def test_element_has_correct_text(driver):
    assert element2.text == "value"
```

### 4. Use Page Object Methods

```python
# ❌ Bad - Direct WebDriver in tests
def test_login(driver):
    driver.find_element(By.ID, "username").send_keys("user")
    driver.find_element(By.ID, "password").send_keys("pass")
    driver.find_element(By.ID, "login").click()

# ✅ Good - Use page object
def test_login(driver):
    login_page = LoginPage(driver)
    login_page.login("user", "pass")
```

### 5. Explicit Waits

```python
# ❌ Bad - Sleep
import time
time.sleep(5)

# ✅ Good - Explicit wait
self.wait_for_element_visible(locator)
```

---

## Advanced Features

### Parallel Execution

```bash
# Run with 4 workers
pytest -n 4

# Auto-detect CPU cores
pytest -n auto

# Distribute by file
pytest -n auto --dist loadfile
```

### Rerun Failures

```bash
# Rerun failed tests 2 times with 5 second delay
pytest --reruns 2 --reruns-delay 5
```

### Custom Command Line Options

```python
# In conftest.py
def pytest_addoption(parser):
    parser.addoption("--custom", action="store", help="Custom option")

@pytest.fixture
def custom_option(request):
    return request.config.getoption("--custom")

# Usage
pytest --custom=value
```

### Taking Screenshots

```python
from utils.screenshot import capture_screenshot

def test_example(driver):
    # Your test code
    capture_screenshot(driver, "test_step_1")
    # More test code
```

---

## Examples

See complete examples in the `tests/` directory:
- `test_login.py` - Login functionality tests
- `test_products.py` - Product page tests
- `test_e2e_workflow.py` - End-to-end workflow tests

---

**Questions?** Check [SETUP.md](SETUP.md) or open an issue on GitHub.