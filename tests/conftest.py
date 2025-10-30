"""
Conftest - Pytest Fixtures and Hooks
Contains pytest fixtures, hooks, and configurations for test execution
"""

import pytest
import os
from datetime import datetime
from pathlib import Path
from selenium.webdriver.remote.webdriver import WebDriver
from core.browser_factory import BrowserFactory
from config.config import config
from utils.logger import logger
from utils.screenshot import capture_screenshot


# Command line options
def pytest_addoption(parser):
    """Add custom command line options"""
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Browser to run tests: chrome, firefox, edge, safari"
    )
    parser.addoption(
        "--headless",
        action="store",
        default="false",
        help="Run browser in headless mode: true or false"
    )
    parser.addoption(
        "--env",
        action="store",
        default="dev",
        help="Environment to run tests: dev, staging, prod"
    )


@pytest.fixture(scope="session", autouse=True)
def setup_environment(request):
    """Setup test environment from command line options"""
    browser = request.config.getoption("--browser")
    headless = request.config.getoption("--headless").lower() == "true"
    env = request.config.getoption("--env")
    
    # Set environment variables
    os.environ['BROWSER'] = browser
    os.environ['HEADLESS'] = str(headless)
    os.environ['ENV'] = env
    
    logger.info("=" * 80)
    logger.info(f"TEST EXECUTION STARTED")
    logger.info(f"Browser: {browser}")
    logger.info(f"Headless: {headless}")
    logger.info(f"Environment: {env}")
    logger.info(f"Base URL: {config.base_url}")
    logger.info("=" * 80)
    
    yield
    
    logger.info("=" * 80)
    logger.info("TEST EXECUTION COMPLETED")
    logger.info("=" * 80)


@pytest.fixture(scope="function")
def driver(request):
    """
    WebDriver fixture - creates and tears down driver for each test
    
    Usage in test:
        def test_example(driver):
            driver.get("https://example.com")
    """
    browser = config.browser
    headless = config.headless
    
    logger.info(f"Initializing WebDriver for test: {request.node.name}")
    
    # Initialize driver
    driver_instance = BrowserFactory.get_driver(browser, headless)
    
    # Make driver available to test
    yield driver_instance
    
    # Teardown
    logger.info(f"Closing WebDriver for test: {request.node.name}")
    BrowserFactory.quit_driver(driver_instance)


@pytest.fixture(scope="class")
def class_driver(request):
    """
    Class-level WebDriver fixture - creates driver once per test class
    Useful for test classes where tests need to share driver state
    
    Usage:
        @pytest.mark.usefixtures("class_driver")
        class TestSuite:
            def test_one(self):
                self.driver.get("https://example.com")
    """
    browser = config.browser
    headless = config.headless
    
    logger.info(f"Initializing class-level WebDriver for: {request.cls.__name__}")
    
    driver_instance = BrowserFactory.get_driver(browser, headless)
    request.cls.driver = driver_instance
    
    yield driver_instance
    
    logger.info(f"Closing class-level WebDriver for: {request.cls.__name__}")
    BrowserFactory.quit_driver(driver_instance)


# Pytest Hooks

def pytest_runtest_setup(item):
    """Hook that runs before each test"""
    logger.info("")
    logger.info("*" * 80)
    logger.info(f"STARTING TEST: {item.name}")
    logger.info("*" * 80)


def pytest_runtest_teardown(item, nextitem):
    """Hook that runs after each test"""
    logger.info("*" * 80)
    logger.info(f"COMPLETED TEST: {item.name}")
    logger.info("*" * 80)
    logger.info("")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook to capture test results and take screenshots on failure
    """
    outcome = yield
    report = outcome.get_result()
    
    # Only capture screenshots for test call phase (not setup/teardown)
    if report.when == "call":
        # Get the driver fixture if available
        driver_fixture = None
        if hasattr(item, 'funcargs') and 'driver' in item.funcargs:
            driver_fixture = item.funcargs['driver']
        elif hasattr(item, 'instance') and hasattr(item.instance, 'driver'):
            driver_fixture = item.instance.driver
        
        # Capture screenshot on failure
        if report.failed and driver_fixture:
            logger.error(f"TEST FAILED: {item.name}")
            test_name = item.name
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            screenshot_name = f"{test_name}_{timestamp}"
            
            try:
                screenshot_path = capture_screenshot(driver_fixture, screenshot_name)
                logger.info(f"Screenshot saved: {screenshot_path}")
                
                # Attach screenshot to Allure report if available
                try:
                    import allure
                    allure.attach.file(
                        screenshot_path,
                        name=screenshot_name,
                        attachment_type=allure.attachment_type.PNG
                    )
                except ImportError:
                    pass
            except Exception as e:
                logger.error(f"Failed to capture screenshot: {str(e)}")
        
        # Log test result
        if report.passed:
            logger.info(f"TEST PASSED: {item.name}")
        elif report.failed:
            logger.error(f"TEST FAILED: {item.name}")
            if report.longrepr:
                logger.error(f"Failure reason: {report.longrepr}")
        elif report.skipped:
            logger.warning(f"TEST SKIPPED: {item.name}")


def pytest_configure(config):
    """Configure pytest with custom settings"""
    # Create directories if they don't exist
    Path('reports').mkdir(exist_ok=True)
    Path('screenshots').mkdir(exist_ok=True)
    Path('logs').mkdir(exist_ok=True)
    
    # Register custom markers
    config.addinivalue_line("markers", "smoke: Quick smoke tests")
    config.addinivalue_line("markers", "regression: Full regression suite")
    config.addinivalue_line("markers", "critical: Critical path tests")


def pytest_collection_modifyitems(config, items):
    """Modify test collection - can be used to skip tests based on conditions"""
    skip_in_ci = pytest.mark.skip(reason="Skipped in CI/CD pipeline")
    
    for item in items:
        # Skip tests marked with skip_in_ci when running in CI
        if "skip_in_ci" in item.keywords and os.getenv("CI"):
            item.add_marker(skip_in_ci)


# Session fixtures for test data

@pytest.fixture(scope="session")
def test_users():
    """
    Fixture providing test user credentials
    
    Returns:
        Dictionary of test users
    """
    return {
        "standard_user": {
            "username": "standard_user",
            "password": "secret_sauce"
        },
        "locked_out_user": {
            "username": "locked_out_user",
            "password": "secret_sauce"
        },
        "problem_user": {
            "username": "problem_user",
            "password": "secret_sauce"
        },
        "performance_glitch_user": {
            "username": "performance_glitch_user",
            "password": "secret_sauce"
        }
    }


@pytest.fixture(scope="session")
def invalid_credentials():
    """
    Fixture providing invalid test credentials
    
    Returns:
        Dictionary of invalid credentials
    """
    return {
        "invalid_user": {
            "username": "invalid_user",
            "password": "invalid_password"
        },
        "empty_username": {
            "username": "",
            "password": "secret_sauce"
        },
        "empty_password": {
            "username": "standard_user",
            "password": ""
        },
        "empty_both": {
            "username": "",
            "password": ""
        }
    }


# Helper fixtures

@pytest.fixture
def wait_time():
    """Fixture providing custom wait time"""
    return config.timeout


@pytest.fixture
def base_url():
    """Fixture providing base URL"""
    return config.base_url