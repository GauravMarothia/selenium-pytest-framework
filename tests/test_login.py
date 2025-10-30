"""
Login Tests
Test cases for login functionality
"""

import pytest
from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from utils.logger import logger


@pytest.mark.smoke
@pytest.mark.critical
class TestLogin:
    """Test suite for login functionality"""
    
    def test_successful_login_with_standard_user(self, driver, test_users):
        """
        Test successful login with valid credentials
        
        Steps:
            1. Navigate to login page
            2. Enter valid username and password
            3. Click login button
            4. Verify user is redirected to products page
        """
        logger.info("Starting test: Successful login with standard user")
        
        login_page = LoginPage(driver)
        products_page = ProductsPage(driver)
        
        # Get test credentials
        user = test_users["standard_user"]
        
        # Perform login
        login_page.navigate()
        assert login_page.is_displayed(), "Login page is not displayed"
        
        login_page.login(user["username"], user["password"])
        
        # Verify redirect to products page
        assert products_page.is_displayed(), "Products page is not displayed after login"
        assert "inventory.html" in products_page.get_current_url(), "URL does not contain inventory"
        
        logger.info("Test passed: User successfully logged in")
    
    @pytest.mark.smoke
    def test_login_with_locked_out_user(self, driver, test_users):
        """
        Test login with locked out user
        
        Steps:
            1. Navigate to login page
            2. Enter locked out user credentials
            3. Click login button
            4. Verify error message is displayed
        """
        logger.info("Starting test: Login with locked out user")
        
        login_page = LoginPage(driver)
        user = test_users["locked_out_user"]
        
        login_page.navigate()
        login_page.login(user["username"], user["password"])
        
        # Verify error message
        assert login_page.is_error_displayed(), "Error message is not displayed"
        error_message = login_page.get_error_message()
        assert "locked out" in error_message.lower(), f"Unexpected error message: {error_message}"
        
        logger.info("Test passed: Correct error displayed for locked out user")
    
    @pytest.mark.regression
    def test_login_with_invalid_username(self, driver, invalid_credentials):
        """Test login with invalid username"""
        logger.info("Starting test: Login with invalid username")
        
        login_page = LoginPage(driver)
        creds = invalid_credentials["invalid_user"]
        
        login_page.navigate()
        login_page.login(creds["username"], creds["password"])
        
        # Verify error message
        assert login_page.is_error_displayed(), "Error message is not displayed"
        error_message = login_page.get_error_message()
        assert "Username and password do not match" in error_message, \
            f"Unexpected error message: {error_message}"
        
        logger.info("Test passed: Correct error for invalid credentials")
    
    @pytest.mark.regression
    def test_login_with_empty_username(self, driver, invalid_credentials):
        """Test login with empty username"""
        logger.info("Starting test: Login with empty username")
        
        login_page = LoginPage(driver)
        creds = invalid_credentials["empty_username"]
        
        login_page.navigate()
        login_page.login(creds["username"], creds["password"])
        
        # Verify error message
        assert login_page.is_error_displayed(), "Error message is not displayed"
        error_message = login_page.get_error_message()
        assert "Username is required" in error_message, f"Unexpected error message: {error_message}"
        
        logger.info("Test passed: Correct error for empty username")
    
    @pytest.mark.regression
    def test_login_with_empty_password(self, driver, invalid_credentials):
        """Test login with empty password"""
        logger.info("Starting test: Login with empty password")
        
        login_page = LoginPage(driver)
        creds = invalid_credentials["empty_password"]
        
        login_page.navigate()
        login_page.login(creds["username"], creds["password"])
        
        # Verify error message
        assert login_page.is_error_displayed(), "Error message is not displayed"
        error_message = login_page.get_error_message()
        assert "Password is required" in error_message, f"Unexpected error message: {error_message}"
        
        logger.info("Test passed: Correct error for empty password")
    
    @pytest.mark.regression
    def test_login_with_empty_credentials(self, driver, invalid_credentials):
        """Test login with both fields empty"""
        logger.info("Starting test: Login with empty credentials")
        
        login_page = LoginPage(driver)
        creds = invalid_credentials["empty_both"]
        
        login_page.navigate()
        login_page.login(creds["username"], creds["password"])
        
        # Verify error message
        assert login_page.is_error_displayed(), "Error message is not displayed"
        error_message = login_page.get_error_message()
        assert "Username is required" in error_message, f"Unexpected error message: {error_message}"
        
        logger.info("Test passed: Correct error for empty credentials")
    
    @pytest.mark.smoke
    def test_logout_functionality(self, driver, test_users):
        """
        Test logout functionality
        
        Steps:
            1. Login with valid credentials
            2. Click logout from menu
            3. Verify user is redirected to login page
        """
        logger.info("Starting test: Logout functionality")
        
        login_page = LoginPage(driver)
        products_page = ProductsPage(driver)
        user = test_users["standard_user"]
        
        # Login
        login_page.navigate()
        login_page.login(user["username"], user["password"])
        assert products_page.is_displayed(), "Products page not displayed"
        
        # Logout
        products_page.logout()
        
        # Verify redirect to login page
        assert login_page.is_displayed(), "Login page is not displayed after logout"
        assert "saucedemo.com" in login_page.get_current_url(), "URL incorrect after logout"
        
        logger.info("Test passed: User successfully logged out")
    
    @pytest.mark.regression
    def test_error_message_can_be_closed(self, driver, invalid_credentials):
        """Test that error message can be closed"""
        logger.info("Starting test: Error message can be closed")
        
        login_page = LoginPage(driver)
        creds = invalid_credentials["invalid_user"]
        
        login_page.navigate()
        login_page.login(creds["username"], creds["password"])
        
        # Verify error is displayed
        assert login_page.is_error_displayed(), "Error message is not displayed"
        
        # Close error message
        login_page.close_error_message()
        
        # Verify error is no longer displayed
        assert not login_page.is_error_displayed(), "Error message still displayed after closing"
        
        logger.info("Test passed: Error message can be closed")