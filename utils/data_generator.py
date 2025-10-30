"""
Test Data Generator
Generates random test data for various testing scenarios
"""

from faker import Faker
import random
import string
from datetime import datetime, timedelta
from typing import Dict, List
from utils.logger import logger


class DataGenerator:
    """Generate random test data"""
    
    def __init__(self, locale: str = 'en_US'):
        """
        Initialize data generator
        
        Args:
            locale: Locale for faker library
        """
        self.fake = Faker(locale)
        logger.debug(f"DataGenerator initialized with locale: {locale}")
    
    # User Data Generation
    
    def generate_user(self) -> Dict[str, str]:
        """
        Generate random user data
        
        Returns:
            Dictionary with user information
        """
        user = {
            'first_name': self.fake.first_name(),
            'last_name': self.fake.last_name(),
            'email': self.fake.email(),
            'username': self.fake.user_name(),
            'password': self.generate_password(),
            'phone': self.fake.phone_number(),
            'date_of_birth': self.fake.date_of_birth(minimum_age=18, maximum_age=80).strftime('%Y-%m-%d')
        }
        logger.debug(f"Generated user: {user['username']}")
        return user
    
    def generate_password(self, length: int = 12, 
                         include_special: bool = True,
                         include_numbers: bool = True,
                         include_uppercase: bool = True) -> str:
        """
        Generate random password
        
        Args:
            length: Password length
            include_special: Include special characters
            include_numbers: Include numbers
            include_uppercase: Include uppercase letters
        
        Returns:
            Generated password
        """
        characters = string.ascii_lowercase
        
        if include_uppercase:
            characters += string.ascii_uppercase
        if include_numbers:
            characters += string.digits
        if include_special:
            characters += "!@#$%^&*"
        
        password = ''.join(random.choice(characters) for _ in range(length))
        return password
    
    def generate_email(self, domain: str = None) -> str:
        """
        Generate random email address
        
        Args:
            domain: Email domain (optional)
        
        Returns:
            Email address
        """
        if domain:
            return f"{self.fake.user_name()}@{domain}"
        return self.fake.email()
    
    # Address Data Generation
    
    def generate_address(self) -> Dict[str, str]:
        """
        Generate random address
        
        Returns:
            Dictionary with address information
        """
        address = {
            'street_address': self.fake.street_address(),
            'city': self.fake.city(),
            'state': self.fake.state(),
            'zip_code': self.fake.zipcode(),
            'country': self.fake.country()
        }
        logger.debug(f"Generated address in: {address['city']}")
        return address
    
    # Payment Data Generation
    
    def generate_credit_card(self) -> Dict[str, str]:
        """
        Generate random credit card data (for testing only!)
        
        Returns:
            Dictionary with credit card information
        """
        card = {
            'card_number': self.fake.credit_card_number(),
            'card_type': self.fake.credit_card_provider(),
            'cvv': ''.join(random.choices(string.digits, k=3)),
            'expiry_month': random.randint(1, 12),
            'expiry_year': random.randint(2024, 2030),
            'cardholder_name': self.fake.name()
        }
        logger.debug(f"Generated {card['card_type']} card")
        return card
    
    # Company Data Generation
    
    def generate_company(self) -> Dict[str, str]:
        """
        Generate random company data
        
        Returns:
            Dictionary with company information
        """
        company = {
            'name': self.fake.company(),
            'email': self.fake.company_email(),
            'phone': self.fake.phone_number(),
            'website': self.fake.url(),
            'industry': random.choice(['Technology', 'Finance', 'Healthcare', 'Retail', 'Manufacturing'])
        }
        logger.debug(f"Generated company: {company['name']}")
        return company
    
    # Product Data Generation
    
    def generate_product(self) -> Dict[str, any]:
        """
        Generate random product data
        
        Returns:
            Dictionary with product information
        """
        product = {
            'name': f"{self.fake.word().capitalize()} {self.fake.word().capitalize()}",
            'description': self.fake.text(max_nb_chars=200),
            'price': round(random.uniform(10.0, 999.99), 2),
            'sku': ''.join(random.choices(string.ascii_uppercase + string.digits, k=8)),
            'category': random.choice(['Electronics', 'Clothing', 'Books', 'Home', 'Sports']),
            'quantity': random.randint(1, 100)
        }
        logger.debug(f"Generated product: {product['name']}")
        return product
    
    # Text Data Generation
    
    def generate_text(self, sentences: int = 3) -> str:
        """
        Generate random text
        
        Args:
            sentences: Number of sentences
        
        Returns:
            Generated text
        """
        return self.fake.text(max_nb_chars=sentences * 50)
    
    def generate_sentence(self) -> str:
        """Generate random sentence"""
        return self.fake.sentence()
    
    def generate_paragraph(self) -> str:
        """Generate random paragraph"""
        return self.fake.paragraph()
    
    # Date/Time Generation
    
    def generate_date(self, start_date: str = '-30d', end_date: str = 'today') -> str:
        """
        Generate random date
        
        Args:
            start_date: Start date (relative or absolute)
            end_date: End date (relative or absolute)
        
        Returns:
            Date string (YYYY-MM-DD)
        """
        date = self.fake.date_between(start_date=start_date, end_date=end_date)
        return date.strftime('%Y-%m-%d')
    
    def generate_future_date(self, days: int = 30) -> str:
        """
        Generate future date
        
        Args:
            days: Number of days in future
        
        Returns:
            Future date string
        """
        future_date = datetime.now() + timedelta(days=days)
        return future_date.strftime('%Y-%m-%d')
    
    def generate_past_date(self, days: int = 30) -> str:
        """
        Generate past date
        
        Args:
            days: Number of days in past
        
        Returns:
            Past date string
        """
        past_date = datetime.now() - timedelta(days=days)
        return past_date.strftime('%Y-%m-%d')
    
    # Numeric Data Generation
    
    def generate_random_number(self, min_value: int = 1, max_value: int = 100) -> int:
        """Generate random integer"""
        return random.randint(min_value, max_value)
    
    def generate_random_float(self, min_value: float = 1.0, 
                             max_value: float = 100.0, 
                             decimals: int = 2) -> float:
        """Generate random float"""
        return round(random.uniform(min_value, max_value), decimals)
    
    # List Generation
    
    def generate_user_list(self, count: int = 5) -> List[Dict[str, str]]:
        """
        Generate list of users
        
        Args:
            count: Number of users to generate
        
        Returns:
            List of user dictionaries
        """
        return [self.generate_user() for _ in range(count)]
    
    def generate_product_list(self, count: int = 5) -> List[Dict[str, any]]:
        """
        Generate list of products
        
        Args:
            count: Number of products to generate
        
        Returns:
            List of product dictionaries
        """
        return [self.generate_product() for _ in range(count)]
    
    # Unique Data Generation
    
    def generate_unique_email(self, prefix: str = "test") -> str:
        """
        Generate unique email with timestamp
        
        Args:
            prefix: Email prefix
        
        Returns:
            Unique email address
        """
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        return f"{prefix}_{timestamp}@test.com"
    
    def generate_unique_username(self, prefix: str = "user") -> str:
        """
        Generate unique username with timestamp
        
        Args:
            prefix: Username prefix
        
        Returns:
            Unique username
        """
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        return f"{prefix}_{timestamp}"
    
    # Phone Number Generation
    
    def generate_phone_number(self, country_code: str = "+1") -> str:
        """
        Generate phone number
        
        Args:
            country_code: Country code prefix
        
        Returns:
            Phone number string
        """
        number = ''.join(random.choices(string.digits, k=10))
        return f"{country_code} ({number[:3]}) {number[3:6]}-{number[6:]}"
    
    # URL Generation
    
    def generate_url(self) -> str:
        """Generate random URL"""
        return self.fake.url()
    
    def generate_image_url(self, width: int = 640, height: int = 480) -> str:
        """
        Generate placeholder image URL
        
        Args:
            width: Image width
            height: Image height
        
        Returns:
            Image URL
        """
        return f"https://via.placeholder.com/{width}x{height}"
    
    # File Generation
    
    def generate_filename(self, extension: str = "txt") -> str:
        """
        Generate random filename
        
        Args:
            extension: File extension
        
        Returns:
            Filename string
        """
        name = ''.join(random.choices(string.ascii_lowercase, k=10))
        return f"{name}.{extension}"


# Global instance
data_generator = DataGenerator()