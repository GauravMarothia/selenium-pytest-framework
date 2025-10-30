"""
Base Page Object
Parent class for all page objects with common methods and utilities
"""

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from config.config import config
from utils.logger import logger
from typing import List, Tuple


class BasePage:
    """Base page class with common page interactions"""
    
    def __init__(self, driver):
        """
        Initialize base page
        
        Args:
            driver: Selenium WebDriver instance
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, config.timeout)
        self.actions = ActionChains(driver)
    
    # Navigation Methods
    
    def navigate_to(self, url: str):
        """Navigate to specific URL"""
        logger.info(f"Navigating to: {url}")
        self.driver.get(url)
    
    def navigate_to_base_url(self):
        """Navigate to base URL from config"""
        self.navigate_to(config.base_url)
    
    def get_current_url(self) -> str:
        """Get current page URL"""
        return self.driver.current_url
    
    def get_page_title(self) -> str:
        """Get current page title"""
        return self.driver.title
    
    def refresh_page(self):
        """Refresh the current page"""
        logger.info("Refreshing page")
        self.driver.refresh()
    
    def go_back(self):
        """Navigate back in browser history"""
        logger.info("Navigating back")
        self.driver.back()
    
    def go_forward(self):
        """Navigate forward in browser history"""
        logger.info("Navigating forward")
        self.driver.forward()
    
    # Element Finding Methods
    
    def find_element(self, locator: Tuple[By, str], timeout: int = None):
        """
        Find element with explicit wait
        
        Args:
            locator: Tuple of (By, locator_value)
            timeout: Custom timeout in seconds
        
        Returns:
            WebElement if found
        """
        timeout = timeout or config.timeout
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            logger.debug(f"Element found: {locator}")
            return element
        except TimeoutException:
            logger.error(f"Element not found: {locator}")
            raise
    
    def find_elements(self, locator: Tuple[By, str], timeout: int = None) -> List:
        """
        Find multiple elements with explicit wait
        
        Args:
            locator: Tuple of (By, locator_value)
            timeout: Custom timeout in seconds
        
        Returns:
            List of WebElements
        """
        timeout = timeout or config.timeout
        try:
            elements = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_all_elements_located(locator)
            )
            logger.debug(f"Found {len(elements)} elements: {locator}")
            return elements
        except TimeoutException:
            logger.error(f"Elements not found: {locator}")
            return []
    
    def is_element_present(self, locator: Tuple[By, str], timeout: int = 5) -> bool:
        """
        Check if element is present on page
        
        Args:
            locator: Tuple of (By, locator_value)
            timeout: Custom timeout in seconds
        
        Returns:
            True if element present, False otherwise
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False
    
    def is_element_visible(self, locator: Tuple[By, str], timeout: int = None) -> bool:
        """
        Check if element is visible on page
        
        Args:
            locator: Tuple of (By, locator_value)
            timeout: Custom timeout in seconds
        
        Returns:
            True if element visible, False otherwise
        """
        timeout = timeout or config.timeout
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False
    
    # Element Interaction Methods
    
    def click(self, locator: Tuple[By, str], timeout: int = None):
        """
        Click on element
        
        Args:
            locator: Tuple of (By, locator_value)
            timeout: Custom timeout in seconds
        """
        timeout = timeout or config.timeout
        element = WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )
        logger.info(f"Clicking element: {locator}")
        element.click()
    
    def type_text(self, locator: Tuple[By, str], text: str, timeout: int = None, clear_first: bool = True):
        """
        Type text into element
        
        Args:
            locator: Tuple of (By, locator_value)
            text: Text to type
            timeout: Custom timeout in seconds
            clear_first: Clear field before typing
        """
        element = self.find_element(locator, timeout)
        if clear_first:
            element.clear()
        logger.info(f"Typing text into element: {locator}")
        element.send_keys(text)
    
    def get_text(self, locator: Tuple[By, str], timeout: int = None) -> str:
        """
        Get text from element
        
        Args:
            locator: Tuple of (By, locator_value)
            timeout: Custom timeout in seconds
        
        Returns:
            Element text
        """
        element = self.find_element(locator, timeout)
        text = element.text
        logger.debug(f"Got text from element {locator}: {text}")
        return text
    
    def get_attribute(self, locator: Tuple[By, str], attribute: str, timeout: int = None) -> str:
        """
        Get attribute value from element
        
        Args:
            locator: Tuple of (By, locator_value)
            attribute: Attribute name
            timeout: Custom timeout in seconds
        
        Returns:
            Attribute value
        """
        element = self.find_element(locator, timeout)
        value = element.get_attribute(attribute)
        logger.debug(f"Got attribute '{attribute}' from element {locator}: {value}")
        return value
    
    def clear_field(self, locator: Tuple[By, str], timeout: int = None):
        """Clear input field"""
        element = self.find_element(locator, timeout)
        logger.info(f"Clearing field: {locator}")
        element.clear()
    
    # Advanced Interaction Methods
    
    def hover_over_element(self, locator: Tuple[By, str], timeout: int = None):
        """
        Hover mouse over element
        
        Args:
            locator: Tuple of (By, locator_value)
            timeout: Custom timeout in seconds
        """
        element = self.find_element(locator, timeout)
        logger.info(f"Hovering over element: {locator}")
        self.actions.move_to_element(element).perform()
    
    def double_click_element(self, locator: Tuple[By, str], timeout: int = None):
        """Double click on element"""
        element = self.find_element(locator, timeout)
        logger.info(f"Double clicking element: {locator}")
        self.actions.double_click(element).perform()
    
    def right_click_element(self, locator: Tuple[By, str], timeout: int = None):
        """Right click on element"""
        element = self.find_element(locator, timeout)
        logger.info(f"Right clicking element: {locator}")
        self.actions.context_click(element).perform()
    
    def drag_and_drop(self, source_locator: Tuple[By, str], target_locator: Tuple[By, str], timeout: int = None):
        """
        Drag and drop element
        
        Args:
            source_locator: Source element locator
            target_locator: Target element locator
            timeout: Custom timeout in seconds
        """
        source = self.find_element(source_locator, timeout)
        target = self.find_element(target_locator, timeout)
        logger.info(f"Dragging {source_locator} to {target_locator}")
        self.actions.drag_and_drop(source, target).perform()
    
    def press_key(self, locator: Tuple[By, str], key: str, timeout: int = None):
        """
        Press keyboard key on element
        
        Args:
            locator: Tuple of (By, locator_value)
            key: Key to press (use Keys class)
            timeout: Custom timeout in seconds
        """
        element = self.find_element(locator, timeout)
        logger.info(f"Pressing key {key} on element: {locator}")
        element.send_keys(key)
    
    # Wait Methods
    
    def wait_for_element_visible(self, locator: Tuple[By, str], timeout: int = None):
        """Wait until element is visible"""
        timeout = timeout or config.timeout
        logger.info(f"Waiting for element to be visible: {locator}")
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )
    
    def wait_for_element_invisible(self, locator: Tuple[By, str], timeout: int = None):
        """Wait until element is invisible"""
        timeout = timeout or config.timeout
        logger.info(f"Waiting for element to be invisible: {locator}")
        return WebDriverWait(self.driver, timeout).until(
            EC.invisibility_of_element_located(locator)
        )
    
    def wait_for_text_in_element(self, locator: Tuple[By, str], text: str, timeout: int = None):
        """Wait until specific text appears in element"""
        timeout = timeout or config.timeout
        logger.info(f"Waiting for text '{text}' in element: {locator}")
        return WebDriverWait(self.driver, timeout).until(
            EC.text_to_be_present_in_element(locator, text)
        )
    
    # JavaScript Execution Methods
    
    def execute_script(self, script: str, *args):
        """
        Execute JavaScript code
        
        Args:
            script: JavaScript code to execute
            *args: Arguments to pass to script
        
        Returns:
            Script execution result
        """
        logger.debug(f"Executing script: {script}")
        return self.driver.execute_script(script, *args)
    
    def scroll_to_element(self, locator: Tuple[By, str], timeout: int = None):
        """Scroll to element using JavaScript"""
        element = self.find_element(locator, timeout)
        logger.info(f"Scrolling to element: {locator}")
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
    
    def scroll_to_bottom(self):
        """Scroll to bottom of page"""
        logger.info("Scrolling to bottom of page")
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
    def scroll_to_top(self):
        """Scroll to top of page"""
        logger.info("Scrolling to top of page")
        self.driver.execute_script("window.scrollTo(0, 0);")
    
    def click_with_js(self, locator: Tuple[By, str], timeout: int = None):
        """Click element using JavaScript (useful when normal click fails)"""
        element = self.find_element(locator, timeout)
        logger.info(f"Clicking element with JavaScript: {locator}")
        self.driver.execute_script("arguments[0].click();", element)
    
    # Frame/Window Handling
    
    def switch_to_frame(self, frame_locator: Tuple[By, str], timeout: int = None):
        """Switch to iframe"""
        timeout = timeout or config.timeout
        logger.info(f"Switching to frame: {frame_locator}")
        WebDriverWait(self.driver, timeout).until(
            EC.frame_to_be_available_and_switch_to_it(frame_locator)
        )
    
    def switch_to_default_content(self):
        """Switch back to main content from iframe"""
        logger.info("Switching to default content")
        self.driver.switch_to.default_content()
    
    def switch_to_window(self, window_handle: str):
        """Switch to specific window"""
        logger.info(f"Switching to window: {window_handle}")
        self.driver.switch_to.window(window_handle)
    
    def get_window_handles(self) -> List[str]:
        """Get all window handles"""
        return self.driver.window_handles
    
    # Alert Handling
    
    def accept_alert(self, timeout: int = None):
        """Accept JavaScript alert"""
        timeout = timeout or config.timeout
        logger.info("Accepting alert")
        WebDriverWait(self.driver, timeout).until(EC.alert_is_present())
        self.driver.switch_to.alert.accept()
    
    def dismiss_alert(self, timeout: int = None):
        """Dismiss JavaScript alert"""
        timeout = timeout or config.timeout
        logger.info("Dismissing alert")
        WebDriverWait(self.driver, timeout).until(EC.alert_is_present())
        self.driver.switch_to.alert.dismiss()
    
    def get_alert_text(self, timeout: int = None) -> str:
        """Get alert text"""
        timeout = timeout or config.timeout
        WebDriverWait(self.driver, timeout).until(EC.alert_is_present())
        alert_text = self.driver.switch_to.alert.text
        logger.info(f"Alert text: {alert_text}")
        return alert_text