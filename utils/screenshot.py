"""
Screenshot Utility
Handles capturing and saving screenshots during test execution
"""

import os
from pathlib import Path
from datetime import datetime
from selenium.webdriver.remote.webdriver import WebDriver
from utils.logger import logger


def capture_screenshot(driver: WebDriver, name: str = None, directory: str = "screenshots") -> str:
    """
    Capture screenshot and save to file
    
    Args:
        driver: WebDriver instance
        name: Screenshot name (without extension)
        directory: Directory to save screenshot
    
    Returns:
        Path to saved screenshot
    """
    # Create screenshots directory if it doesn't exist
    screenshot_dir = Path(directory)
    screenshot_dir.mkdir(exist_ok=True)
    
    # Generate filename
    if name is None:
        name = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    # Ensure .png extension
    if not name.endswith('.png'):
        name = f"{name}.png"
    
    screenshot_path = screenshot_dir / name
    
    try:
        # Capture screenshot
        driver.save_screenshot(str(screenshot_path))
        logger.info(f"Screenshot captured: {screenshot_path}")
        return str(screenshot_path)
    except Exception as e:
        logger.error(f"Failed to capture screenshot: {str(e)}")
        raise


def capture_element_screenshot(driver: WebDriver, element, name: str = None, directory: str = "screenshots") -> str:
    """
    Capture screenshot of specific element
    
    Args:
        driver: WebDriver instance
        element: WebElement to capture
        name: Screenshot name (without extension)
        directory: Directory to save screenshot
    
    Returns:
        Path to saved screenshot
    """
    # Create screenshots directory
    screenshot_dir = Path(directory)
    screenshot_dir.mkdir(exist_ok=True)
    
    # Generate filename
    if name is None:
        name = f"element_screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    if not name.endswith('.png'):
        name = f"{name}.png"
    
    screenshot_path = screenshot_dir / name
    
    try:
        # Capture element screenshot
        element.screenshot(str(screenshot_path))
        logger.info(f"Element screenshot captured: {screenshot_path}")
        return str(screenshot_path)
    except Exception as e:
        logger.error(f"Failed to capture element screenshot: {str(e)}")
        raise


def capture_full_page_screenshot(driver: WebDriver, name: str = None, directory: str = "screenshots") -> str:
    """
    Capture full page screenshot (including parts not visible in viewport)
    
    Args:
        driver: WebDriver instance
        name: Screenshot name (without extension)
        directory: Directory to save screenshot
    
    Returns:
        Path to saved screenshot
    """
    # Create screenshots directory
    screenshot_dir = Path(directory)
    screenshot_dir.mkdir(exist_ok=True)
    
    # Generate filename
    if name is None:
        name = f"fullpage_screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    if not name.endswith('.png'):
        name = f"{name}.png"
    
    screenshot_path = screenshot_dir / name
    
    try:
        # Get original size
        original_size = driver.get_window_size()
        
        # Get full page dimensions
        total_width = driver.execute_script("return document.body.scrollWidth")
        total_height = driver.execute_script("return document.body.scrollHeight")
        
        # Set window size to full page
        driver.set_window_size(total_width, total_height)
        
        # Capture screenshot
        driver.save_screenshot(str(screenshot_path))
        
        # Restore original window size
        driver.set_window_size(original_size['width'], original_size['height'])
        
        logger.info(f"Full page screenshot captured: {screenshot_path}")
        return str(screenshot_path)
    except Exception as e:
        logger.error(f"Failed to capture full page screenshot: {str(e)}")
        # Restore window size on error
        try:
            driver.set_window_size(original_size['width'], original_size['height'])
        except:
            pass
        raise