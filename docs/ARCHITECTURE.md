# Framework Architecture

Comprehensive documentation of the Selenium PyTest Framework architecture, design patterns, and implementation details.

---

## Table of Contents

1. [Overview](#overview)
2. [Design Patterns](#design-patterns)
3. [Architecture Layers](#architecture-layers)
4. [Component Details](#component-details)
5. [Data Flow](#data-flow)
6. [Design Decisions](#design-decisions)
7. [Scalability](#scalability)
8. [Extension Points](#extension-points)

---

## Overview

This framework implements a **layered architecture** with clear separation of concerns, following industry best practices for maintainable and scalable test automation.

### Key Principles

- **DRY (Don't Repeat Yourself)** - Reusable components and utilities
- **SOLID Principles** - Single responsibility, open for extension
- **Separation of Concerns** - Clear boundaries between layers
- **Dependency Injection** - Fixtures provide dependencies
- **Configuration Over Code** - External configuration management

---

## Design Patterns

### 1. Page Object Model (POM)

**Purpose:** Encapsulate page-specific logic and elements

**Implementation:**
```
BasePage (Abstract)
    ↓
LoginPage, ProductsPage, DashboardPage (Concrete)
    ↓
Tests
```

**Benefits:**
- Reduces code duplication
- Improves maintainability
- Makes tests more readable
- Simplifies updates when UI changes

**Example:**
```python
class LoginPage(BasePage):
    # Locators
    USERNAME = (By.ID, "username")
    PASSWORD = (By.ID, "password")
    
    # Actions
    def login(self, username, password):
        self.type_text(self.USERNAME, username)
        self.type_text(self.PASSWORD, password)
        self.click(self.LOGIN_BUTTON)
```

### 2. Factory Pattern

**Purpose:** Create WebDriver instances with different configurations

**Implementation:**
```python
class BrowserFactory:
    @staticmethod
    def get_driver(browser, headless):
        if browser == 'chrome':
            return _get_chrome_driver(headless)
        elif browser == 'firefox':
            return _get_firefox_driver(headless)
```

**Benefits:**
- Centralized driver creation
- Easy to add new browsers
- Consistent configuration

### 3. Singleton Pattern

**Purpose:** Single configuration instance across framework

**Implementation:**
```python
class Config:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
```

**Benefits:**
- Single source of truth
- Prevents configuration conflicts
- Memory efficient

### 4. Template Method Pattern

**Purpose:** Define test structure with customizable steps

**Implementation:**
```python
class BasePage:
    def find_element(self, locator):
        # Template method with standard flow
        element = self.wait.until(
            EC.presence_of_element_located(locator)
        )
        return element
```

### 5. Strategy Pattern

**Purpose:** Different wait strategies for different scenarios

**Implementation:**
```python
class CustomWaitConditions:
    @staticmethod
    def element_text_to_be(locator, text):
        # Different wait strategy
```

---

## Architecture Layers

### Layer 1: Test Layer (Highest)

**Purpose:** Business logic and test scenarios

**Components:**
- `tests/test_*.py` - Test files
- `tests/conftest.py` - Fixtures and hooks

**Responsibilities:**
- Define test scenarios
- Assert expected outcomes
- Use page objects
- Minimal selenium interaction

**Example:**
```python
def test_login(driver):
    login_page = LoginPage(driver)
    login_page.navigate()
    login_page.login("user", "pass")
    assert dashboard_page.is_displayed()
```

### Layer 2: Page Object Layer

**Purpose:** Page-specific logic and element interactions

**Components:**
- `pages/*.py` - Page object classes

**Responsibilities:**
- Define locators
- Implement page actions
- Return data to tests
- Handle page navigation

**Example:**
```python
class LoginPage(BasePage):
    def login(self, username, password):
        self.type_text(self.USERNAME, username)
        self.type_text(self.PASSWORD, password)
        self.click(self.LOGIN_BUTTON)
```

### Layer 3: Core Layer

**Purpose:** Framework foundation and reusable components

**Components:**
- `core/base_page.py` - Base page class
- `core/browser_factory.py` - Driver factory
- `core/element_actions.py` - Element interactions
- `core/waits.py` - Wait conditions

**Responsibilities:**
- Provide base functionality
- Handle WebDriver operations
- Manage waits and synchronization
- Offer reusable utilities

### Layer 4: Utility Layer

**Purpose:** Supporting utilities and helpers

**Components:**
- `utils/logger.py` - Logging
- `utils/screenshot.py` - Screenshot capture
- `utils/data_generator.py` - Test data
- `utils/report_helper.py` - Reporting

**Responsibilities:**
- Logging operations
- Screenshot management
- Test data generation
- Report generation

### Layer 5: Configuration Layer (Foundation)

**Purpose:** Framework configuration and settings

**Components:**
- `config/config.py` - Configuration manager
- `config/environments.json` - Environment settings

**Responsibilities:**
- Manage environment configuration
- Provide settings to other layers
- Handle multi-environment support

---

## Component Details

### Core Components

#### BasePage
**Purpose:** Parent class for all page objects

**Key Methods:**
- `find_element()` - Find element with wait
- `click()` - Click with retry logic
- `type_text()` - Type with clear option
- `wait_for_element_visible()` - Explicit wait
- `execute_script()` - JavaScript execution

**Design:**
```python
BasePage
├── Navigation methods
├── Element finding methods
├── Interaction methods
├── Wait methods
├── JavaScript methods
└── Frame/Alert handling
```

#### BrowserFactory
**Purpose:** Create configured WebDriver instances

**Supported Browsers:**
- Chrome (default)
- Firefox
- Edge
- Safari

**Configuration Options:**
- Headless mode
- Window size
- Browser preferences
- Performance settings

#### Configuration Manager
**Purpose:** Centralized configuration management

**Features:**
- Multi-environment support
- Environment variables
- JSON configuration
- Singleton pattern

**Access Pattern:**
```python
from config.config import config

base_url = config.base_url
timeout = config.timeout
browser = config.browser
```

### Utility Components

#### Logger
**Purpose:** Structured logging with colors and file output

**Features:**
- Console output with colors
- File output with timestamps
- Multiple log levels
- Automatic file rotation

#### Screenshot Utility
**Purpose:** Capture and save screenshots

**Capabilities:**
- Full page screenshots
- Element screenshots
- Automatic failure capture
- Timestamped filenames

#### Data Generator
**Purpose:** Generate realistic test data

**Data Types:**
- User profiles
- Addresses
- Credit cards (test only)
- Products
- Random text/numbers

---

## Data Flow

### Test Execution Flow

```
1. Pytest Collection
   ├── Discover test files
   ├── Load fixtures
   └── Configure pytest

2. Setup Phase (conftest.py)
   ├── Load configuration
   ├── Initialize WebDriver
   ├── Setup logging
   └── Prepare test data

3. Test Execution
   ├── Navigate to page (Page Object)
   ├── Interact with elements (BasePage)
   ├── Perform assertions (Test)
   └── Log operations (Logger)

4. Teardown Phase
   ├── Capture screenshot (if failed)
   ├── Close WebDriver
   ├── Generate reports
   └── Cleanup resources
```

### Request Flow

```
Test
  ↓ (calls)
Page Object Method
  ↓ (uses)
BasePage Method
  ↓ (executes)
WebDriver Command
  ↓ (interacts)
Browser
```

### Configuration Flow

```
environments.json
  ↓ (loaded by)
Config Manager
  ↓ (accessed by)
All Components
```

---

## Design Decisions

### 1. Why Page Object Model?

**Decision:** Use POM for UI abstraction

**Rationale:**
- **Maintainability:** Changes in UI require updates in one place
- **Reusability:** Page methods used across multiple tests
- **Readability:** Tests read like user stories
- **Separation:** Test logic separate from page logic

**Trade-offs:**
- Initial setup time
- More classes to manage
- Learning curve for team

### 2. Why Explicit Waits?

**Decision:** Use explicit waits over implicit waits or sleep

**Rationale:**
- **Reliability:** Wait for specific conditions
- **Performance:** Don't wait longer than necessary
- **Flexibility:** Different waits for different scenarios
- **Debugging:** Clear wait failures

**Implementation:**
```python
WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable(locator)
)
```

### 3. Why Pytest?

**Decision:** Use Pytest as test runner

**Rationale:**
- **Fixtures:** Powerful dependency injection
- **Markers:** Easy test categorization
- **Plugins:** Rich ecosystem
- **Assertions:** Clear, readable assertions
- **Parallel:** Built-in parallel execution

**Benefits:**
- Simple test syntax
- Great reporting
- Active community
- CI/CD integration

### 4. Why JSON Configuration?

**Decision:** Use JSON for environment configuration

**Rationale:**
- **Readable:** Easy to understand
- **Portable:** Works across platforms
- **Standard:** No special parsing needed
- **Version Control:** Track configuration changes

**Alternative Considered:** YAML (more complex, not necessary)

### 5. Why Docker?

**Decision:** Support Docker containerization

**Rationale:**
- **Consistency:** Same environment everywhere
- **Isolation:** No dependency conflicts
- **CI/CD:** Easy integration
- **Scalability:** Parallel containers

---

## Scalability

### Horizontal Scalability

**Parallel Execution:**
```bash
pytest -n auto  # Auto-detect CPU cores
pytest -n 8     # Specific worker count
```

**Implementation:**
- Uses pytest-xdist
- Tests must be independent
- Shared resources handled via fixtures

### Vertical Scalability

**Test Organization:**
```
tests/
├── smoke/
├── regression/
├── integration/
└── e2e/
```

**Benefits:**
- Run specific suites
- Faster feedback
- Better organization

### Cloud Scalability

**Integration Points:**
```python
# BrowserStack, Sauce Labs, etc.
def get_remote_driver(capabilities):
    return webdriver.Remote(
        command_executor=REMOTE_URL,
        desired_capabilities=capabilities
    )
```

---

## Extension Points

### Adding New Page Objects

1. Inherit from BasePage
2. Define locators as class variables
3. Implement page-specific methods
4. Follow naming conventions

```python
class NewPage(BasePage):
    # Locators
    ELEMENT = (By.ID, "element-id")
    
    # Methods
    def action(self):
        self.click(self.ELEMENT)
```

### Adding New Browsers

1. Add method to BrowserFactory
2. Configure browser options
3. Return WebDriver instance

```python
@staticmethod
def _get_new_browser_driver(headless):
    options = NewBrowserOptions()
    # Configure options
    return webdriver.NewBrowser(options=options)
```

### Adding New Wait Conditions

1. Add to CustomWaitConditions
2. Implement predicate function
3. Document usage

```python
@staticmethod
def custom_condition(locator, value):
    def _predicate(driver):
        # Custom logic
        return True/False
    return _predicate
```

### Adding New Utilities

1. Create new file in utils/
2. Implement utility class
3. Add documentation
4. Export if needed

---

## Best Practices

### Code Organization

✅ **DO:**
- One page object per page
- Clear, descriptive names
- Consistent file structure
- Comprehensive docstrings

❌ **DON'T:**
- Mix test and page logic
- Use sleep() statements
- Hard-code test data
- Ignore exceptions

### Performance

✅ **DO:**
- Use appropriate waits
- Run tests in parallel
- Minimize browser restarts
- Cache static data

❌ **DON'T:**
- Use long timeouts unnecessarily
- Run all tests sequentially
- Create new driver per test method
- Make external API calls in loops

### Maintenance

✅ **DO:**
- Keep locators up to date
- Review and refactor regularly
- Update documentation
- Version control everything

❌ **DON'T:**
- Let dead code accumulate
- Ignore flaky tests
- Skip code reviews
- Forget to update docs

---

## Troubleshooting Architecture Issues

### Common Issues

**Circular Imports:**
```python
# Solution: Import at function level
def method():
    from module import Class
```

**Stale Element References:**
```python
# Solution: Re-find element
element = self.find_element(locator)  # Finds fresh element
```

**Timeout Issues:**
```python
# Solution: Adjust wait times
self.wait_for_element_visible(locator, timeout=30)
```

---

## Future Enhancements

1. **API Testing Layer** - Add REST API test support
2. **Mobile Testing** - Integrate Appium
3. **Visual Testing** - Add visual regression
4. **AI/ML** - Self-healing locators
5. **Performance** - Integrate Lighthouse
6. **Database** - Add DB validation layer

---

**Questions about architecture?** Open an issue on [GitHub](https://github.com/yourprofile/selenium-pytest-framework/issues)