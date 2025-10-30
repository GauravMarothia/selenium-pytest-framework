"""
Browser Factory
Handles WebDriver initialization for different browsers with various configurations
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from config.config import config
from utils.logger import logger


class BrowserFactory:
    """Factory class to create WebDriver instances"""
    
    @staticmethod
    def get_driver(browser: str = None, headless: bool = None):
        """
        Create and return a WebDriver instance
        
        Args:
            browser: Browser name (chrome, firefox, edge, safari)
            headless: Run browser in headless mode
        
        Returns:
            WebDriver instance
        """
        browser = browser or config.browser
        headless = headless if headless is not None else config.headless
        
        logger.info(f"Initializing {browser} browser (headless: {headless})")
        
        if browser == 'chrome':
            return BrowserFactory._get_chrome_driver(headless)
        elif browser == 'firefox':
            return BrowserFactory._get_firefox_driver(headless)
        elif browser == 'edge':
            return BrowserFactory._get_edge_driver(headless)
        elif browser == 'safari':
            return BrowserFactory._get_safari_driver()
        else:
            raise ValueError(f"Unsupported browser: {browser}")
    
    @staticmethod
    def _get_chrome_driver(headless: bool):
        """Create Chrome WebDriver with options"""
        options = ChromeOptions()
        
        # Performance optimizations
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-infobars')
        options.add_argument('--start-maximized')
        
        # Privacy and security
        options.add_argument('--incognito')
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_experimental_option('useAutomationExtension', False)
        
        # Disable automation flags
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        # Headless mode
        if headless:
            options.add_argument('--headless=new')
            options.add_argument('--window-size=1920,1080')
        
        # Additional preferences
        prefs = {
            'download.default_directory': '/tmp',
            'download.prompt_for_download': False,
            'profile.default_content_setting_values.notifications': 2,
            'profile.default_content_settings.popups': 0
        }
        options.add_experimental_option('prefs', prefs)
        
        driver = webdriver.Chrome(options=options)
        driver.maximize_window()
        driver.implicitly_wait(config.timeout)
        
        logger.info("Chrome driver initialized successfully")
        return driver
    
    @staticmethod
    def _get_firefox_driver(headless: bool):
        """Create Firefox WebDriver with options"""
        options = FirefoxOptions()
        
        # Performance optimizations
        options.add_argument('--width=1920')
        options.add_argument('--height=1080')
        
        # Privacy
        options.set_preference('browser.privatebrowsing.autostart', True)
        options.set_preference('dom.webnotifications.enabled', False)
        
        # Headless mode
        if headless:
            options.add_argument('--headless')
        
        driver = webdriver.Firefox(options=options)
        driver.maximize_window()
        driver.implicitly_wait(config.timeout)
        
        logger.info("Firefox driver initialized successfully")
        return driver
    
    @staticmethod
    def _get_edge_driver(headless: bool):
        """Create Edge WebDriver with options"""
        options = EdgeOptions()
        
        # Performance optimizations
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--start-maximized')
        
        # Privacy
        options.add_argument('--inprivate')
        
        # Headless mode
        if headless:
            options.add_argument('--headless')
            options.add_argument('--window-size=1920,1080')
        
        driver = webdriver.Edge(options=options)
        driver.maximize_window()
        driver.implicitly_wait(config.timeout)
        
        logger.info("Edge driver initialized successfully")
        return driver
    
    @staticmethod
    def _get_safari_driver():
        """Create Safari WebDriver"""
        driver = webdriver.Safari()
        driver.maximize_window()
        driver.implicitly_wait(config.timeout)
        
        logger.info("Safari driver initialized successfully")
        return driver
    
    @staticmethod
    def quit_driver(driver):
        """Safely quit the WebDriver"""
        if driver:
            try:
                driver.quit()
                logger.info("WebDriver closed successfully")
            except Exception as e:
                logger.error(f"Error closing WebDriver: {str(e)}")