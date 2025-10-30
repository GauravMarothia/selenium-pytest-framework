"""
Element Actions
Custom element interaction methods with enhanced reliability and error handling
"""

from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import (
    StaleElementReferenceException,
    ElementClickInterceptedException,
    ElementNotInteractableException
)
from typing import List, Tuple
from utils.logger import logger
import time


class ElementActions:
    """Enhanced element interaction methods"""
    
    def __init__(self, driver):
        """
        Initialize element actions
        
        Args:
            driver: Selenium WebDriver instance
        """
        self.driver = driver
        self.actions = ActionChains(driver)
    
    def safe_click(self, element: WebElement, retry_count: int = 3) -> bool:
        """
        Click element with retry mechanism for reliability
        
        Args:
            element: WebElement to click
            retry_count: Number of retry attempts
        
        Returns:
            True if click successful, False otherwise
        """
        for attempt in range(retry_count):
            try:
                element.click()
                logger.debug(f"Click successful on attempt {attempt + 1}")
                return True
            except (StaleElementReferenceException, ElementClickInterceptedException) as e:
                logger.warning(f"Click attempt {attempt + 1} failed: {str(e)}")
                if attempt == retry_count - 1:
                    logger.error("All click attempts failed")
                    # Try JavaScript click as last resort
                    try:
                        self.driver.execute_script("arguments[0].click();", element)
                        logger.info("JavaScript click successful")
                        return True
                    except Exception as js_error:
                        logger.error(f"JavaScript click failed: {str(js_error)}")
                        return False
                time.sleep(0.5)
        return False
    
    def safe_send_keys(self, element: WebElement, text: str, clear_first: bool = True, 
                       retry_count: int = 3) -> bool:
        """
        Send keys to element with retry mechanism
        
        Args:
            element: WebElement to type into
            text: Text to send
            clear_first: Clear field before typing
            retry_count: Number of retry attempts
        
        Returns:
            True if successful, False otherwise
        """
        for attempt in range(retry_count):
            try:
                if clear_first:
                    element.clear()
                element.send_keys(text)
                logger.debug(f"Send keys successful on attempt {attempt + 1}")
                return True
            except (StaleElementReferenceException, ElementNotInteractableException) as e:
                logger.warning(f"Send keys attempt {attempt + 1} failed: {str(e)}")
                if attempt == retry_count - 1:
                    logger.error("All send keys attempts failed")
                    return False
                time.sleep(0.5)
        return False
    
    def select_dropdown_by_text(self, element: WebElement, text: str) -> bool:
        """
        Select dropdown option by visible text
        
        Args:
            element: Select element
            text: Visible text to select
        
        Returns:
            True if successful
        """
        try:
            select = Select(element)
            select.select_by_visible_text(text)
            logger.info(f"Selected dropdown option: {text}")
            return True
        except Exception as e:
            logger.error(f"Failed to select dropdown option: {str(e)}")
            return False
    
    def select_dropdown_by_value(self, element: WebElement, value: str) -> bool:
        """
        Select dropdown option by value attribute
        
        Args:
            element: Select element
            value: Value attribute to select
        
        Returns:
            True if successful
        """
        try:
            select = Select(element)
            select.select_by_value(value)
            logger.info(f"Selected dropdown value: {value}")
            return True
        except Exception as e:
            logger.error(f"Failed to select dropdown value: {str(e)}")
            return False
    
    def select_dropdown_by_index(self, element: WebElement, index: int) -> bool:
        """
        Select dropdown option by index
        
        Args:
            element: Select element
            index: Index to select (0-based)
        
        Returns:
            True if successful
        """
        try:
            select = Select(element)
            select.select_by_index(index)
            logger.info(f"Selected dropdown index: {index}")
            return True
        except Exception as e:
            logger.error(f"Failed to select dropdown index: {str(e)}")
            return False
    
    def get_dropdown_options(self, element: WebElement) -> List[str]:
        """
        Get all options from dropdown
        
        Args:
            element: Select element
        
        Returns:
            List of option texts
        """
        try:
            select = Select(element)
            options = [option.text for option in select.options]
            logger.debug(f"Found {len(options)} dropdown options")
            return options
        except Exception as e:
            logger.error(f"Failed to get dropdown options: {str(e)}")
            return []
    
    def get_selected_dropdown_option(self, element: WebElement) -> str:
        """
        Get currently selected dropdown option
        
        Args:
            element: Select element
        
        Returns:
            Selected option text
        """
        try:
            select = Select(element)
            selected = select.first_selected_option.text
            logger.debug(f"Selected option: {selected}")
            return selected
        except Exception as e:
            logger.error(f"Failed to get selected option: {str(e)}")
            return ""
    
    def checkbox_select(self, element: WebElement) -> bool:
        """
        Select checkbox if not already selected
        
        Args:
            element: Checkbox element
        
        Returns:
            True if successful
        """
        try:
            if not element.is_selected():
                element.click()
                logger.info("Checkbox selected")
            else:
                logger.debug("Checkbox already selected")
            return True
        except Exception as e:
            logger.error(f"Failed to select checkbox: {str(e)}")
            return False
    
    def checkbox_deselect(self, element: WebElement) -> bool:
        """
        Deselect checkbox if selected
        
        Args:
            element: Checkbox element
        
        Returns:
            True if successful
        """
        try:
            if element.is_selected():
                element.click()
                logger.info("Checkbox deselected")
            else:
                logger.debug("Checkbox already deselected")
            return True
        except Exception as e:
            logger.error(f"Failed to deselect checkbox: {str(e)}")
            return False
    
    def radio_button_select(self, element: WebElement) -> bool:
        """
        Select radio button
        
        Args:
            element: Radio button element
        
        Returns:
            True if successful
        """
        try:
            if not element.is_selected():
                element.click()
                logger.info("Radio button selected")
            return True
        except Exception as e:
            logger.error(f"Failed to select radio button: {str(e)}")
            return False
    
    def hover_and_click(self, hover_element: WebElement, click_element: WebElement) -> bool:
        """
        Hover over one element and click another
        
        Args:
            hover_element: Element to hover over
            click_element: Element to click
        
        Returns:
            True if successful
        """
        try:
            self.actions.move_to_element(hover_element).perform()
            time.sleep(0.5)  # Brief pause for menu to appear
            click_element.click()
            logger.info("Hover and click successful")
            return True
        except Exception as e:
            logger.error(f"Hover and click failed: {str(e)}")
            return False
    
    def drag_and_drop_by_offset(self, element: WebElement, x_offset: int, y_offset: int) -> bool:
        """
        Drag element by pixel offset
        
        Args:
            element: Element to drag
            x_offset: Horizontal offset in pixels
            y_offset: Vertical offset in pixels
        
        Returns:
            True if successful
        """
        try:
            self.actions.drag_and_drop_by_offset(element, x_offset, y_offset).perform()
            logger.info(f"Drag and drop by offset successful: ({x_offset}, {y_offset})")
            return True
        except Exception as e:
            logger.error(f"Drag and drop by offset failed: {str(e)}")
            return False
    
    def send_special_key(self, element: WebElement, key: str) -> bool:
        """
        Send special key to element (ENTER, TAB, ESC, etc.)
        
        Args:
            element: Target element
            key: Special key from Keys class
        
        Returns:
            True if successful
        """
        try:
            element.send_keys(key)
            logger.info(f"Special key sent: {key}")
            return True
        except Exception as e:
            logger.error(f"Failed to send special key: {str(e)}")
            return False
    
    def clear_field_with_backspace(self, element: WebElement) -> bool:
        """
        Clear field by sending backspace keys (useful when .clear() doesn't work)
        
        Args:
            element: Input element
        
        Returns:
            True if successful
        """
        try:
            current_value = element.get_attribute("value")
            if current_value:
                for _ in range(len(current_value)):
                    element.send_keys(Keys.BACK_SPACE)
            logger.info("Field cleared with backspace")
            return True
        except Exception as e:
            logger.error(f"Failed to clear field with backspace: {str(e)}")
            return False
    
    def scroll_element_into_center(self, element: WebElement) -> bool:
        """
        Scroll element into center of viewport
        
        Args:
            element: Element to scroll to
        
        Returns:
            True if successful
        """
        try:
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center', inline: 'center'});",
                element
            )
            time.sleep(0.3)  # Brief pause for scroll
            logger.info("Element scrolled into center")
            return True
        except Exception as e:
            logger.error(f"Failed to scroll element into center: {str(e)}")
            return False
    
    def highlight_element(self, element: WebElement, duration: float = 2.0) -> None:
        """
        Highlight element temporarily (useful for debugging)
        
        Args:
            element: Element to highlight
            duration: How long to highlight (seconds)
        """
        try:
            original_style = element.get_attribute("style")
            self.driver.execute_script(
                "arguments[0].setAttribute('style', arguments[1]);",
                element,
                "border: 3px solid red; background-color: yellow;"
            )
            time.sleep(duration)
            self.driver.execute_script(
                "arguments[0].setAttribute('style', arguments[1]);",
                element,
                original_style
            )
            logger.debug("Element highlighted")
        except Exception as e:
            logger.error(f"Failed to highlight element: {str(e)}")
    
    def is_element_clickable(self, element: WebElement) -> bool:
        """
        Check if element is clickable (displayed and enabled)
        
        Args:
            element: Element to check
        
        Returns:
            True if clickable
        """
        try:
            return element.is_displayed() and element.is_enabled()
        except Exception:
            return False