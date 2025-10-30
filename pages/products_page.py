"""
Products Page Object
Page object for the products/inventory page
"""

from selenium.webdriver.common.by import By
from core.base_page import BasePage
from utils.logger import logger
from typing import List


class ProductsPage(BasePage):
    """Products page object class"""
    
    # Locators
    PAGE_TITLE = (By.CLASS_NAME, "title")
    PRODUCT_ITEMS = (By.CLASS_NAME, "inventory_item")
    PRODUCT_NAMES = (By.CLASS_NAME, "inventory_item_name")
    PRODUCT_PRICES = (By.CLASS_NAME, "inventory_item_price")
    ADD_TO_CART_BUTTONS = (By.CSS_SELECTOR, "button[id^='add-to-cart']")
    REMOVE_BUTTONS = (By.CSS_SELECTOR, "button[id^='remove']")
    SHOPPING_CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    SHOPPING_CART_LINK = (By.CLASS_NAME, "shopping_cart_link")
    BURGER_MENU = (By.ID, "react-burger-menu-btn")
    LOGOUT_LINK = (By.ID, "logout_sidebar_link")
    PRODUCT_SORT_DROPDOWN = (By.CLASS_NAME, "product_sort_container")
    
    def __init__(self, driver):
        """Initialize products page"""
        super().__init__(driver)
    
    def is_displayed(self) -> bool:
        """
        Check if products page is displayed
        
        Returns:
            True if products page is displayed
        """
        logger.info("Checking if products page is displayed")
        return self.is_element_visible(self.PAGE_TITLE) and \
               "Products" in self.get_text(self.PAGE_TITLE)
    
    def get_page_title(self) -> str:
        """
        Get page title text
        
        Returns:
            Page title
        """
        return self.get_text(self.PAGE_TITLE)
    
    def get_product_count(self) -> int:
        """
        Get total number of products
        
        Returns:
            Number of products
        """
        products = self.find_elements(self.PRODUCT_ITEMS)
        count = len(products)
        logger.info(f"Found {count} products")
        return count
    
    def get_all_product_names(self) -> List[str]:
        """
        Get all product names
        
        Returns:
            List of product names
        """
        elements = self.find_elements(self.PRODUCT_NAMES)
        names = [elem.text for elem in elements]
        logger.info(f"Product names: {names}")
        return names
    
    def get_all_product_prices(self) -> List[str]:
        """
        Get all product prices
        
        Returns:
            List of product prices
        """
        elements = self.find_elements(self.PRODUCT_PRICES)
        prices = [elem.text for elem in elements]
        logger.info(f"Product prices: {prices}")
        return prices
    
    def add_product_to_cart_by_name(self, product_name: str):
        """
        Add product to cart by product name
        
        Args:
            product_name: Name of the product
        """
        logger.info(f"Adding product to cart: {product_name}")
        # Convert product name to button ID format
        product_id = product_name.lower().replace(' ', '-')
        add_button = (By.ID, f"add-to-cart-{product_id}")
        self.click(add_button)
        return self
    
    def remove_product_from_cart_by_name(self, product_name: str):
        """
        Remove product from cart by product name
        
        Args:
            product_name: Name of the product
        """
        logger.info(f"Removing product from cart: {product_name}")
        product_id = product_name.lower().replace(' ', '-')
        remove_button = (By.ID, f"remove-{product_id}")
        self.click(remove_button)
        return self
    
    def add_first_n_products_to_cart(self, count: int = 1):
        """
        Add first N products to cart
        
        Args:
            count: Number of products to add
        """
        logger.info(f"Adding first {count} products to cart")
        buttons = self.find_elements(self.ADD_TO_CART_BUTTONS)
        for i in range(min(count, len(buttons))):
            buttons[i].click()
        return self
    
    def get_cart_item_count(self) -> int:
        """
        Get number of items in cart
        
        Returns:
            Number of items in cart badge
        """
        if self.is_element_present(self.SHOPPING_CART_BADGE, timeout=2):
            count = int(self.get_text(self.SHOPPING_CART_BADGE))
            logger.info(f"Cart item count: {count}")
            return count
        logger.info("Cart is empty")
        return 0
    
    def click_shopping_cart(self):
        """Click shopping cart icon"""
        logger.info("Clicking shopping cart")
        self.click(self.SHOPPING_CART_LINK)
        return self
    
    def open_burger_menu(self):
        """Open burger menu"""
        logger.info("Opening burger menu")
        self.click(self.BURGER_MENU)
        return self
    
    def logout(self):
        """Logout from the application"""
        logger.info("Logging out")
        self.open_burger_menu()
        self.click(self.LOGOUT_LINK)
        return self
    
    def sort_products(self, sort_option: str):
        """
        Sort products by specific option
        
        Args:
            sort_option: Sort option (az, za, lohi, hilo)
        """
        logger.info(f"Sorting products by: {sort_option}")
        from selenium.webdriver.support.ui import Select
        dropdown = self.find_element(self.PRODUCT_SORT_DROPDOWN)
        select = Select(dropdown)
        select.select_by_value(sort_option)
        return self
    
    def is_product_in_cart(self, product_name: str) -> bool:
        """
        Check if product is in cart (has Remove button)
        
        Args:
            product_name: Product name
        
        Returns:
            True if product is in cart
        """
        product_id = product_name.lower().replace(' ', '-')
        remove_button = (By.ID, f"remove-{product_id}")
        return self.is_element_present(remove_button, timeout=2)