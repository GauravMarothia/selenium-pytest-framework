"""
Dashboard Page Object
Page object for the dashboard/products page (after login)
"""

from selenium.webdriver.common.by import By
from core.base_page import BasePage
from utils.logger import logger


class DashboardPage(BasePage):
    """Dashboard page object class"""
    
    # Locators
    APP_LOGO = (By.CLASS_NAME, "app_logo")
    PAGE_TITLE = (By.CLASS_NAME, "title")
    SHOPPING_CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    SHOPPING_CART_LINK = (By.CLASS_NAME, "shopping_cart_link")
    BURGER_MENU_BUTTON = (By.ID, "react-burger-menu-btn")
    LOGOUT_LINK = (By.ID, "logout_sidebar_link")
    ALL_ITEMS_LINK = (By.ID, "inventory_sidebar_link")
    ABOUT_LINK = (By.ID, "about_sidebar_link")
    RESET_APP_LINK = (By.ID, "reset_sidebar_link")
    PRODUCT_SORT_CONTAINER = (By.CLASS_NAME, "product_sort_container")
    INVENTORY_ITEMS = (By.CLASS_NAME, "inventory_item")
    FOOTER = (By.CLASS_NAME, "footer")
    SOCIAL_TWITTER = (By.CSS_SELECTOR, "a[href*='twitter']")
    SOCIAL_FACEBOOK = (By.CSS_SELECTOR, "a[href*='facebook']")
    SOCIAL_LINKEDIN = (By.CSS_SELECTOR, "a[href*='linkedin']")
    
    def __init__(self, driver):
        """Initialize dashboard page"""
        super().__init__(driver)
    
    def is_displayed(self) -> bool:
        """
        Check if dashboard page is displayed
        
        Returns:
            True if dashboard is displayed
        """
        logger.info("Checking if dashboard page is displayed")
        return self.is_element_visible(self.APP_LOGO, timeout=10) and \
               self.is_element_visible(self.PAGE_TITLE, timeout=5)
    
    def get_page_title(self) -> str:
        """
        Get the page title text
        
        Returns:
            Page title
        """
        title = self.get_text(self.PAGE_TITLE)
        logger.info(f"Dashboard page title: {title}")
        return title
    
    def get_welcome_message(self) -> str:
        """
        Get welcome message (using app logo as proxy)
        
        Returns:
            Welcome message
        """
        # Since SauceDemo doesn't have explicit welcome message,
        # we return app name from logo
        app_name = self.get_text(self.APP_LOGO)
        logger.info(f"App name: {app_name}")
        return app_name
    
    def get_cart_item_count(self) -> int:
        """
        Get number of items in shopping cart
        
        Returns:
            Number of items (0 if empty)
        """
        try:
            if self.is_element_present(self.SHOPPING_CART_BADGE, timeout=2):
                count_text = self.get_text(self.SHOPPING_CART_BADGE)
                count = int(count_text) if count_text else 0
                logger.info(f"Cart item count: {count}")
                return count
        except Exception as e:
            logger.debug(f"No items in cart or error: {str(e)}")
        return 0
    
    def click_shopping_cart(self):
        """Navigate to shopping cart"""
        logger.info("Clicking shopping cart")
        self.click(self.SHOPPING_CART_LINK)
        return self
    
    def open_menu(self):
        """Open burger menu"""
        logger.info("Opening burger menu")
        self.click(self.BURGER_MENU_BUTTON)
        # Wait for menu to be visible
        self.wait_for_element_visible(self.LOGOUT_LINK)
        return self
    
    def logout(self):
        """Logout from application"""
        logger.info("Logging out from dashboard")
        self.open_menu()
        self.click(self.LOGOUT_LINK)
        return self
    
    def navigate_to_all_items(self):
        """Navigate to all items page"""
        logger.info("Navigating to all items")
        self.open_menu()
        self.click(self.ALL_ITEMS_LINK)
        return self
    
    def navigate_to_about(self):
        """Navigate to about page"""
        logger.info("Navigating to about page")
        self.open_menu()
        self.click(self.ABOUT_LINK)
        return self
    
    def reset_app_state(self):
        """Reset application state"""
        logger.info("Resetting app state")
        self.open_menu()
        self.click(self.RESET_APP_LINK)
        return self
    
    def get_inventory_count(self) -> int:
        """
        Get number of inventory items displayed
        
        Returns:
            Number of items
        """
        items = self.find_elements(self.INVENTORY_ITEMS)
        count = len(items)
        logger.info(f"Found {count} inventory items")
        return count
    
    def is_footer_displayed(self) -> bool:
        """
        Check if footer is displayed
        
        Returns:
            True if footer visible
        """
        return self.is_element_visible(self.FOOTER, timeout=5)
    
    def get_footer_text(self) -> str:
        """
        Get footer text
        
        Returns:
            Footer text
        """
        return self.get_text(self.FOOTER)
    
    def is_social_links_present(self) -> bool:
        """
        Check if social media links are present
        
        Returns:
            True if all social links present
        """
        twitter = self.is_element_present(self.SOCIAL_TWITTER, timeout=2)
        facebook = self.is_element_present(self.SOCIAL_FACEBOOK, timeout=2)
        linkedin = self.is_element_present(self.SOCIAL_LINKEDIN, timeout=2)
        
        all_present = twitter and facebook and linkedin
        logger.info(f"Social links present: {all_present}")
        return all_present
    
    def click_social_link(self, platform: str):
        """
        Click on social media link
        
        Args:
            platform: Social platform (twitter, facebook, linkedin)
        """
        logger.info(f"Clicking {platform} social link")
        
        social_links = {
            "twitter": self.SOCIAL_TWITTER,
            "facebook": self.SOCIAL_FACEBOOK,
            "linkedin": self.SOCIAL_LINKEDIN
        }
        
        if platform.lower() in social_links:
            self.click(social_links[platform.lower()])
        else:
            logger.error(f"Unknown social platform: {platform}")
        
        return self
    
    def verify_user_logged_in(self) -> bool:
        """
        Verify user is logged in by checking key elements
        
        Returns:
            True if logged in
        """
        logger.info("Verifying user is logged in")
        
        checks = [
            self.is_element_visible(self.APP_LOGO, timeout=5),
            self.is_element_visible(self.BURGER_MENU_BUTTON, timeout=5),
            self.is_element_visible(self.SHOPPING_CART_LINK, timeout=5),
            "inventory" in self.get_current_url().lower()
        ]
        
        is_logged_in = all(checks)
        logger.info(f"User logged in: {is_logged_in}")
        return is_logged_in