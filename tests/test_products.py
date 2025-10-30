"""
Products Tests
Test cases for products/inventory page functionality
"""

import pytest
from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from utils.logger import logger


@pytest.fixture(scope="function")
def logged_in_driver(driver, test_users):
    """
    Fixture that provides a driver with user already logged in
    """
    login_page = LoginPage(driver)
    user = test_users["standard_user"]
    
    login_page.navigate()
    login_page.login(user["username"], user["password"])
    
    return driver


@pytest.mark.regression
class TestProducts:
    """Test suite for products page functionality"""
    
    def test_products_page_displays_correctly(self, logged_in_driver):
        """
        Test that products page displays all expected elements
        
        Steps:
            1. Login to application
            2. Verify products page is displayed
            3. Verify page title is correct
            4. Verify products are displayed
        """
        logger.info("Starting test: Products page displays correctly")
        
        products_page = ProductsPage(logged_in_driver)
        
        # Verify page elements
        assert products_page.is_displayed(), "Products page is not displayed"
        assert products_page.get_page_title() == "Products", "Page title is incorrect"
        
        # Verify products are displayed
        product_count = products_page.get_product_count()
        assert product_count > 0, "No products are displayed"
        logger.info(f"Found {product_count} products on the page")
        
        logger.info("Test passed: Products page displays correctly")
    
    @pytest.mark.smoke
    def test_add_single_product_to_cart(self, logged_in_driver):
        """
        Test adding a single product to cart
        
        Steps:
            1. Login to application
            2. Add one product to cart
            3. Verify cart badge shows correct count
        """
        logger.info("Starting test: Add single product to cart")
        
        products_page = ProductsPage(logged_in_driver)
        
        # Get initial cart count
        initial_count = products_page.get_cart_item_count()
        
        # Add product to cart
        products_page.add_product_to_cart_by_name("sauce-labs-backpack")
        
        # Verify cart count increased
        current_count = products_page.get_cart_item_count()
        assert current_count == initial_count + 1, \
            f"Cart count incorrect. Expected {initial_count + 1}, got {current_count}"
        
        logger.info("Test passed: Product successfully added to cart")
    
    @pytest.mark.smoke
    def test_add_multiple_products_to_cart(self, logged_in_driver):
        """Test adding multiple products to cart"""
        logger.info("Starting test: Add multiple products to cart")
        
        products_page = ProductsPage(logged_in_driver)
        
        # Add 3 products to cart
        products_page.add_first_n_products_to_cart(3)
        
        # Verify cart count
        cart_count = products_page.get_cart_item_count()
        assert cart_count == 3, f"Cart count incorrect. Expected 3, got {cart_count}"
        
        logger.info("Test passed: Multiple products added to cart")
    
    @pytest.mark.regression
    def test_remove_product_from_cart(self, logged_in_driver):
        """
        Test removing product from cart
        
        Steps:
            1. Add product to cart
            2. Remove product from cart
            3. Verify cart count decreases
        """
        logger.info("Starting test: Remove product from cart")
        
        products_page = ProductsPage(logged_in_driver)
        product_name = "sauce-labs-backpack"
        
        # Add product
        products_page.add_product_to_cart_by_name(product_name)
        assert products_page.get_cart_item_count() == 1, "Product not added to cart"
        
        # Remove product
        products_page.remove_product_from_cart_by_name(product_name)
        
        # Verify cart is empty
        cart_count = products_page.get_cart_item_count()
        assert cart_count == 0, f"Cart should be empty, but has {cart_count} items"
        
        logger.info("Test passed: Product successfully removed from cart")
    
    @pytest.mark.regression
    def test_product_names_displayed(self, logged_in_driver):
        """Test that all product names are displayed"""
        logger.info("Starting test: Product names displayed")
        
        products_page = ProductsPage(logged_in_driver)
        
        # Get all product names
        product_names = products_page.get_all_product_names()
        
        # Verify names are not empty
        assert len(product_names) > 0, "No product names found"
        
        for name in product_names:
            assert name and name.strip(), f"Product name is empty or invalid: '{name}'"
        
        logger.info(f"Test passed: Found {len(product_names)} product names")
    
    @pytest.mark.regression
    def test_product_prices_displayed(self, logged_in_driver):
        """Test that all product prices are displayed and valid"""
        logger.info("Starting test: Product prices displayed")
        
        products_page = ProductsPage(logged_in_driver)
        
        # Get all product prices
        prices = products_page.get_all_product_prices()
        
        # Verify prices are not empty and contain $
        assert len(prices) > 0, "No product prices found"
        
        for price in prices:
            assert "$" in price, f"Price doesn't contain $ symbol: {price}"
            # Extract numeric value and verify it's valid
            price_value = price.replace("$", "").strip()
            assert float(price_value) > 0, f"Invalid price value: {price}"
        
        logger.info(f"Test passed: All {len(prices)} prices are valid")
    
    @pytest.mark.regression
    def test_sort_products_by_name_ascending(self, logged_in_driver):
        """Test sorting products by name (A to Z)"""
        logger.info("Starting test: Sort products by name ascending")
        
        products_page = ProductsPage(logged_in_driver)
        
        # Sort by name A-Z
        products_page.sort_products("az")
        
        # Get product names
        product_names = products_page.get_all_product_names()
        
        # Verify names are in ascending order
        sorted_names = sorted(product_names)
        assert product_names == sorted_names, "Products are not sorted in ascending order"
        
        logger.info("Test passed: Products sorted by name (A-Z)")
    
    @pytest.mark.regression
    def test_sort_products_by_name_descending(self, logged_in_driver):
        """Test sorting products by name (Z to A)"""
        logger.info("Starting test: Sort products by name descending")
        
        products_page = ProductsPage(logged_in_driver)
        
        # Sort by name Z-A
        products_page.sort_products("za")
        
        # Get product names
        product_names = products_page.get_all_product_names()
        
        # Verify names are in descending order
        sorted_names = sorted(product_names, reverse=True)
        assert product_names == sorted_names, "Products are not sorted in descending order"
        
        logger.info("Test passed: Products sorted by name (Z-A)")
    
    @pytest.mark.regression
    def test_sort_products_by_price_low_to_high(self, logged_in_driver):
        """Test sorting products by price (low to high)"""
        logger.info("Starting test: Sort products by price (low to high)")
        
        products_page = ProductsPage(logged_in_driver)
        
        # Sort by price low to high
        products_page.sort_products("lohi")
        
        # Get product prices
        price_strings = products_page.get_all_product_prices()
        prices = [float(p.replace("$", "").strip()) for p in price_strings]
        
        # Verify prices are in ascending order
        sorted_prices = sorted(prices)
        assert prices == sorted_prices, "Products are not sorted by price (low to high)"
        
        logger.info("Test passed: Products sorted by price (low to high)")
    
    @pytest.mark.smoke
    def test_shopping_cart_navigation(self, logged_in_driver):
        """Test clicking on shopping cart icon navigates to cart page"""
        logger.info("Starting test: Shopping cart navigation")
        
        products_page = ProductsPage(logged_in_driver)
        
        # Click shopping cart
        products_page.click_shopping_cart()
        
        # Verify navigation to cart page
        current_url = products_page.get_current_url()
        assert "cart.html" in current_url, f"Not navigated to cart page. URL: {current_url}"
        
        logger.info("Test passed: Successfully navigated to cart page")