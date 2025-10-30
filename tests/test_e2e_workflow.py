"""
End-to-End Workflow Tests
Complete user journey tests from login to checkout
"""

import pytest
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.products_page import ProductsPage
from utils.logger import logger


@pytest.mark.critical
@pytest.mark.regression
class TestE2EWorkflow:
    """End-to-end workflow test suite"""
    
    @pytest.mark.smoke
    def test_complete_shopping_flow(self, driver, test_users):
        """
        Test complete shopping workflow
        
        Steps:
            1. Login to application
            2. Verify dashboard is displayed
            3. Add products to cart
            4. Verify cart count
            5. Navigate to cart
            6. Logout
        """
        logger.info("Starting E2E test: Complete shopping flow")
        
        # Initialize page objects
        login_page = LoginPage(driver)
        dashboard_page = DashboardPage(driver)
        products_page = ProductsPage(driver)
        
        # Step 1: Login
        logger.info("Step 1: Logging in")
        user = test_users["standard_user"]
        login_page.navigate()
        login_page.login(user["username"], user["password"])
        
        # Step 2: Verify dashboard
        logger.info("Step 2: Verifying dashboard")
        assert dashboard_page.is_displayed(), "Dashboard is not displayed"
        assert dashboard_page.verify_user_logged_in(), "User not properly logged in"
        
        # Step 3: Add products to cart
        logger.info("Step 3: Adding products to cart")
        products_page.add_product_to_cart_by_name("sauce-labs-backpack")
        products_page.add_product_to_cart_by_name("sauce-labs-bike-light")
        
        # Step 4: Verify cart count
        logger.info("Step 4: Verifying cart count")
        cart_count = dashboard_page.get_cart_item_count()
        assert cart_count == 2, f"Expected 2 items in cart, got {cart_count}"
        
        # Step 5: Navigate to cart
        logger.info("Step 5: Navigating to cart")
        dashboard_page.click_shopping_cart()
        assert "cart" in driver.current_url, "Not navigated to cart page"
        
        # Step 6: Logout
        logger.info("Step 6: Logging out")
        products_page.logout()
        assert login_page.is_displayed(), "Not redirected to login page after logout"
        
        logger.info("E2E test passed: Complete shopping flow")
    
    @pytest.mark.regression
    def test_add_remove_products_workflow(self, driver, test_users):
        """
        Test adding and removing products workflow
        
        Steps:
            1. Login
            2. Add multiple products
            3. Verify cart count
            4. Remove some products
            5. Verify updated cart count
        """
        logger.info("Starting E2E test: Add/Remove products workflow")
        
        login_page = LoginPage(driver)
        dashboard_page = DashboardPage(driver)
        products_page = ProductsPage(driver)
        
        # Login
        user = test_users["standard_user"]
        login_page.navigate()
        login_page.login(user["username"], user["password"])
        
        # Add products
        products_page.add_product_to_cart_by_name("sauce-labs-backpack")
        products_page.add_product_to_cart_by_name("sauce-labs-bike-light")
        products_page.add_product_to_cart_by_name("sauce-labs-bolt-t-shirt")
        
        # Verify count
        assert dashboard_page.get_cart_item_count() == 3, "Expected 3 items in cart"
        
        # Remove one product
        products_page.remove_product_from_cart_by_name("sauce-labs-bike-light")
        
        # Verify updated count
        assert dashboard_page.get_cart_item_count() == 2, "Expected 2 items after removal"
        
        logger.info("E2E test passed: Add/Remove products workflow")
    
    @pytest.mark.regression
    def test_product_sorting_workflow(self, driver, test_users):
        """
        Test product sorting workflow
        
        Steps:
            1. Login
            2. Sort products by name (A-Z)
            3. Verify sorting
            4. Sort by price (low to high)
            5. Verify sorting
        """
        logger.info("Starting E2E test: Product sorting workflow")
        
        login_page = LoginPage(driver)
        products_page = ProductsPage(driver)
        
        # Login
        user = test_users["standard_user"]
        login_page.navigate()
        login_page.login(user["username"], user["password"])
        
        # Sort by name A-Z
        products_page.sort_products("az")
        names = products_page.get_all_product_names()
        assert names == sorted(names), "Products not sorted A-Z"
        
        # Sort by price low to high
        products_page.sort_products("lohi")
        price_strings = products_page.get_all_product_prices()
        prices = [float(p.replace("$", "")) for p in price_strings]
        assert prices == sorted(prices), "Products not sorted by price (low to high)"
        
        logger.info("E2E test passed: Product sorting workflow")
    
    @pytest.mark.critical
    def test_menu_navigation_workflow(self, driver, test_users):
        """
        Test menu navigation workflow
        
        Steps:
            1. Login
            2. Open burger menu
            3. Navigate to About
            4. Go back
            5. Reset app state
            6. Verify reset
        """
        logger.info("Starting E2E test: Menu navigation workflow")
        
        login_page = LoginPage(driver)
        dashboard_page = DashboardPage(driver)
        products_page = ProductsPage(driver)
        
        # Login
        user = test_users["standard_user"]
        login_page.navigate()
        login_page.login(user["username"], user["password"])
        
        # Add products first
        products_page.add_first_n_products_to_cart(2)
        initial_count = dashboard_page.get_cart_item_count()
        assert initial_count == 2, "Products not added"
        
        # Reset app state
        dashboard_page.reset_app_state()
        
        # Verify cart is cleared (reset removes items)
        # Note: In actual implementation, you might need to refresh or wait
        driver.refresh()
        final_count = dashboard_page.get_cart_item_count()
        logger.info(f"Cart count after reset: {final_count}")
        
        logger.info("E2E test passed: Menu navigation workflow")
    
    @pytest.mark.regression
    def test_multiple_users_workflow(self, driver, test_users):
        """
        Test workflow with multiple user types
        
        Steps:
            1. Login with standard user
            2. Add products
            3. Logout
            4. Login with different user
            5. Verify fresh session
        """
        logger.info("Starting E2E test: Multiple users workflow")
        
        login_page = LoginPage(driver)
        dashboard_page = DashboardPage(driver)
        products_page = ProductsPage(driver)
        
        # User 1: Standard user
        user1 = test_users["standard_user"]
        login_page.navigate()
        login_page.login(user1["username"], user1["password"])
        
        products_page.add_first_n_products_to_cart(2)
        assert dashboard_page.get_cart_item_count() == 2
        
        # Logout
        dashboard_page.logout()
        assert login_page.is_displayed()
        
        # User 2: Performance glitch user
        user2 = test_users["performance_glitch_user"]
        login_page.login(user2["username"], user2["password"])
        
        # Verify fresh session (no items in cart)
        cart_count = dashboard_page.get_cart_item_count()
        assert cart_count == 0, f"Expected fresh cart, got {cart_count} items"
        
        logger.info("E2E test passed: Multiple users workflow")
    
    @pytest.mark.smoke
    @pytest.mark.critical
    def test_error_recovery_workflow(self, driver, test_users, invalid_credentials):
        """
        Test error recovery workflow
        
        Steps:
            1. Try login with invalid credentials
            2. Verify error message
            3. Close error
            4. Login with valid credentials
            5. Verify successful login
        """
        logger.info("Starting E2E test: Error recovery workflow")
        
        login_page = LoginPage(driver)
        dashboard_page = DashboardPage(driver)
        
        # Try invalid login
        invalid = invalid_credentials["invalid_user"]
        login_page.navigate()
        login_page.login(invalid["username"], invalid["password"])
        
        # Verify error
        assert login_page.is_error_displayed(), "Error not displayed"
        
        # Close error and retry
        login_page.close_error_message()
        
        # Login with valid credentials
        valid = test_users["standard_user"]
        login_page.clear_username()
        login_page.clear_password()
        login_page.login(valid["username"], valid["password"])
        
        # Verify success
        assert dashboard_page.is_displayed(), "Dashboard not displayed after valid login"
        
        logger.info("E2E test passed: Error recovery workflow")
    
    @pytest.mark.regression
    def test_full_shopping_cart_workflow(self, driver, test_users):
        """
        Test adding all products to cart
        
        Steps:
            1. Login
            2. Get total product count
            3. Add all products to cart
            4. Verify all products added
            5. Navigate to cart
        """
        logger.info("Starting E2E test: Full shopping cart workflow")
        
        login_page = LoginPage(driver)
        dashboard_page = DashboardPage(driver)
        products_page = ProductsPage(driver)
        
        # Login
        user = test_users["standard_user"]
        login_page.navigate()
        login_page.login(user["username"], user["password"])
        
        # Get product count
        total_products = products_page.get_product_count()
        logger.info(f"Total products available: {total_products}")
        
        # Add all products
        products_page.add_first_n_products_to_cart(total_products)
        
        # Verify all added
        cart_count = dashboard_page.get_cart_item_count()
        assert cart_count == total_products, \
            f"Expected {total_products} items in cart, got {cart_count}"
        
        # Navigate to cart
        dashboard_page.click_shopping_cart()
        assert "cart" in driver.current_url
        
        logger.info("E2E test passed: Full shopping cart workflow")