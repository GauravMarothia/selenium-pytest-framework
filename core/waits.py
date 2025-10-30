"""
Custom Wait Conditions
Advanced wait conditions for complex scenarios
"""

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from typing import Tuple, Callable
from utils.logger import logger


class CustomWaitConditions:
    """Custom wait conditions extending Selenium's built-in conditions"""
    
    @staticmethod
    def element_text_to_be(locator: Tuple, text: str):
        """
        Wait until element text matches exactly
        
        Args:
            locator: Tuple of (By, locator_value)
            text: Expected text
        
        Returns:
            Condition function
        """
        def _predicate(driver):
            try:
                element = driver.find_element(*locator)
                return element.text == text
            except NoSuchElementException:
                return False
        return _predicate
    
    @staticmethod
    def element_text_contains(locator: Tuple, text: str):
        """
        Wait until element text contains substring
        
        Args:
            locator: Tuple of (By, locator_value)
            text: Expected substring
        
        Returns:
            Condition function
        """
        def _predicate(driver):
            try:
                element = driver.find_element(*locator)
                return text in element.text
            except NoSuchElementException:
                return False
        return _predicate
    
    @staticmethod
    def element_attribute_to_be(locator: Tuple, attribute: str, value: str):
        """
        Wait until element attribute has specific value
        
        Args:
            locator: Tuple of (By, locator_value)
            attribute: Attribute name
            value: Expected value
        
        Returns:
            Condition function
        """
        def _predicate(driver):
            try:
                element = driver.find_element(*locator)
                return element.get_attribute(attribute) == value
            except NoSuchElementException:
                return False
        return _predicate
    
    @staticmethod
    def element_attribute_contains(locator: Tuple, attribute: str, value: str):
        """
        Wait until element attribute contains value
        
        Args:
            locator: Tuple of (By, locator_value)
            attribute: Attribute name
            value: Expected substring
        
        Returns:
            Condition function
        """
        def _predicate(driver):
            try:
                element = driver.find_element(*locator)
                attr_value = element.get_attribute(attribute)
                return attr_value and value in attr_value
            except NoSuchElementException:
                return False
        return _predicate
    
    @staticmethod
    def number_of_elements_to_be(locator: Tuple, count: int):
        """
        Wait until exact number of elements present
        
        Args:
            locator: Tuple of (By, locator_value)
            count: Expected count
        
        Returns:
            Condition function
        """
        def _predicate(driver):
            try:
                elements = driver.find_elements(*locator)
                return len(elements) == count
            except NoSuchElementException:
                return False
        return _predicate
    
    @staticmethod
    def number_of_elements_more_than(locator: Tuple, count: int):
        """
        Wait until number of elements exceeds count
        
        Args:
            locator: Tuple of (By, locator_value)
            count: Minimum count
        
        Returns:
            Condition function
        """
        def _predicate(driver):
            try:
                elements = driver.find_elements(*locator)
                return len(elements) > count
            except NoSuchElementException:
                return False
        return _predicate
    
    @staticmethod
    def element_to_be_selected(locator: Tuple):
        """
        Wait until element is selected (checkbox/radio)
        
        Args:
            locator: Tuple of (By, locator_value)
        
        Returns:
            Condition function
        """
        def _predicate(driver):
            try:
                element = driver.find_element(*locator)
                return element.is_selected()
            except NoSuchElementException:
                return False
        return _predicate
    
    @staticmethod
    def element_to_be_not_selected(locator: Tuple):
        """
        Wait until element is not selected
        
        Args:
            locator: Tuple of (By, locator_value)
        
        Returns:
            Condition function
        """
        def _predicate(driver):
            try:
                element = driver.find_element(*locator)
                return not element.is_selected()
            except NoSuchElementException:
                return False
        return _predicate
    
    @staticmethod
    def url_contains(substring: str):
        """
        Wait until URL contains substring
        
        Args:
            substring: Expected substring in URL
        
        Returns:
            Condition function
        """
        def _predicate(driver):
            return substring in driver.current_url
        return _predicate
    
    @staticmethod
    def url_matches(pattern: str):
        """
        Wait until URL matches regex pattern
        
        Args:
            pattern: Regex pattern
        
        Returns:
            Condition function
        """
        import re
        def _predicate(driver):
            return re.search(pattern, driver.current_url) is not None
        return _predicate
    
    @staticmethod
    def title_contains(substring: str):
        """
        Wait until page title contains substring
        
        Args:
            substring: Expected substring in title
        
        Returns:
            Condition function
        """
        def _predicate(driver):
            return substring in driver.title
        return _predicate
    
    @staticmethod
    def element_css_property_to_be(locator: Tuple, property_name: str, value: str):
        """
        Wait until element CSS property has specific value
        
        Args:
            locator: Tuple of (By, locator_value)
            property_name: CSS property name
            value: Expected value
        
        Returns:
            Condition function
        """
        def _predicate(driver):
            try:
                element = driver.find_element(*locator)
                return element.value_of_css_property(property_name) == value
            except NoSuchElementException:
                return False
        return _predicate
    
    @staticmethod
    def new_window_is_opened(initial_window_count: int):
        """
        Wait until new window is opened
        
        Args:
            initial_window_count: Initial number of windows
        
        Returns:
            Condition function
        """
        def _predicate(driver):
            return len(driver.window_handles) > initial_window_count
        return _predicate
    
    @staticmethod
    def custom_condition(condition_func: Callable):
        """
        Create custom wait condition from function
        
        Args:
            condition_func: Function that takes driver and returns boolean
        
        Returns:
            Condition function
        """
        return condition_func


class SmartWait:
    """Smart wait wrapper with enhanced error handling and logging"""
    
    def __init__(self, driver, timeout: int = 10, poll_frequency: float = 0.5):
        """
        Initialize smart wait
        
        Args:
            driver: WebDriver instance
            timeout: Maximum wait time in seconds
            poll_frequency: How often to check condition
        """
        self.driver = driver
        self.timeout = timeout
        self.poll_frequency = poll_frequency
    
    def until(self, condition, message: str = "") -> any:
        """
        Wait until condition is true
        
        Args:
            condition: Wait condition
            message: Error message if timeout
        
        Returns:
            Result from condition
        """
        try:
            wait = WebDriverWait(
                self.driver,
                self.timeout,
                poll_frequency=self.poll_frequency
            )
            result = wait.until(condition)
            logger.debug(f"Wait condition met: {message or 'Custom condition'}")
            return result
        except TimeoutException:
            error_msg = f"Timeout waiting for: {message or 'condition'}"
            logger.error(error_msg)
            raise TimeoutException(error_msg)
    
    def until_not(self, condition, message: str = "") -> any:
        """
        Wait until condition becomes false
        
        Args:
            condition: Wait condition
            message: Error message if timeout
        
        Returns:
            Result from condition
        """
        try:
            wait = WebDriverWait(
                self.driver,
                self.timeout,
                poll_frequency=self.poll_frequency
            )
            result = wait.until_not(condition)
            logger.debug(f"Wait condition met (not): {message or 'Custom condition'}")
            return result
        except TimeoutException:
            error_msg = f"Timeout waiting for not: {message or 'condition'}"
            logger.error(error_msg)
            raise TimeoutException(error_msg)
    
    def element_to_be_visible(self, locator: Tuple, message: str = ""):
        """Wait for element to be visible"""
        return self.until(
            EC.visibility_of_element_located(locator),
            message or f"Element visible: {locator}"
        )
    
    def element_to_be_clickable(self, locator: Tuple, message: str = ""):
        """Wait for element to be clickable"""
        return self.until(
            EC.element_to_be_clickable(locator),
            message or f"Element clickable: {locator}"
        )
    
    def element_to_be_invisible(self, locator: Tuple, message: str = ""):
        """Wait for element to be invisible"""
        return self.until(
            EC.invisibility_of_element_located(locator),
            message or f"Element invisible: {locator}"
        )
    
    def text_to_be_present(self, locator: Tuple, text: str, message: str = ""):
        """Wait for text to be present in element"""
        return self.until(
            EC.text_to_be_present_in_element(locator, text),
            message or f"Text '{text}' present in: {locator}"
        )