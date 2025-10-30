"""
Login Page Object
Page object for the login page with locators and actions
"""

from selenium.webdriver.common.by import By
from core.base_page import BasePage
from config.config import config
from utils.logger import logger


class LoginPage(BasePage):
    """Login page object class"""
    
    # Locators
    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")
    ERROR_BUTTON = (By.CSS_SELECTOR, ".error-button")
    LOGIN_LOGO = (By.CLASS_NAME, "login_logo")
    LOGIN_CREDENTIALS = (By.ID, "login_credentials")
    
    def __init__(self, driver):
        """Initialize login page"""
        super().__init__(driver)
        self.url = config.base_url
    
    def navigate(self):
        """Navigate to login page"""
        logger.info(f"Navigating to login page: {self.url}")
        self.navigate_to(self.url)
        return self
    
    def is_displayed(self) -> bool:
        """
        Check if login page is displayed
        
        Returns:
            True if login page is displayed
        """
        logger.info("Checking if login page is displayed")
        return self.is_element_visible(self.LOGIN_LOGO) and \
               self.is_element_visible(self.USERNAME_INPUT)
    
    def enter_username(self, username: str):
        """
        Enter username in the username field
        
        Args:
            username: Username to enter
        """
        logger.info(f"Entering username: {username}")
        self.type_text(self.USERNAME_INPUT, username)
        return self
    
    def enter_password(self, password: str):
        """
        Enter password in the password field
        
        Args:
            password: Password to enter
        """
        logger.info("Entering password")
        self.type_text(self.PASSWORD_INPUT, password)
        return self
    
    def click_login_button(self):
        """Click the login button"""
        logger.info("Clicking login button")
        self.click(self.LOGIN_BUTTON)
        return self
    
    def login(self, username: str, password: str):
        """
        Complete login process
        
        Args:
            username: Username
            password: Password
        """
        logger.info(f"Performing login with username: {username}")
        self.enter_username(username)
        self.enter_password(password)
        self.click_login_button()
        return self
    
    def get_error_message(self) -> str:
        """
        Get error message text
        
        Returns:
            Error message text
        """
        logger.info("Getting error message")
        return self.get_text(self.ERROR_MESSAGE)
    
    def is_error_displayed(self) -> bool:
        """
        Check if error message is displayed
        
        Returns:
            True if error is displayed
        """
        return self.is_element_visible(self.ERROR_MESSAGE, timeout=5)
    
    def close_error_message(self):
        """Close error message"""
        logger.info("Closing error message")
        self.click(self.ERROR_BUTTON)
        return self
    
    def get_available_usernames(self) -> list:
        """
        Get list of available usernames from the login page
        
        Returns:
            List of usernames
        """
        credentials_text = self.get_text(self.LOGIN_CREDENTIALS)
        # Parse usernames from credentials text
        usernames = []
        for line in credentials_text.split('\n'):
            if line and not line.startswith('Accepted'):
                usernames.append(line.strip())
        return usernames
    
    def clear_username(self):
        """Clear username field"""
        logger.info("Clearing username field")
        self.clear_field(self.USERNAME_INPUT)
        return self
    
    def clear_password(self):
        """Clear password field"""
        logger.info("Clearing password field")
        self.clear_field(self.PASSWORD_INPUT)
        return self
    
    def is_login_button_enabled(self) -> bool:
        """
        Check if login button is enabled
        
        Returns:
            True if button is enabled
        """
        return self.find_element(self.LOGIN_BUTTON).is_enabled()