"""
Configuration Manager
Handles loading and managing configuration settings for different environments
"""

import json
import os
from pathlib import Path
from typing import Dict, Any


class Config:
    """Singleton configuration manager for the framework"""
    
    _instance = None
    _config_data = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._config_data is None:
            self._load_config()
    
    def _load_config(self):
        """Load configuration from environments.json file"""
        config_path = Path(__file__).parent / "environments.json"
        
        if not config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
        
        with open(config_path, 'r') as f:
            self._config_data = json.load(f)
    
    def get_env_config(self, env: str = None) -> Dict[str, Any]:
        """
        Get configuration for specific environment
        
        Args:
            env: Environment name (dev, staging, prod)
        
        Returns:
            Dictionary with environment configuration
        """
        if env is None:
            env = os.getenv('ENV', 'dev')
        
        if env not in self._config_data:
            raise ValueError(f"Environment '{env}' not found in configuration")
        
        return self._config_data[env]
    
    def get(self, key: str, env: str = None, default: Any = None) -> Any:
        """
        Get specific configuration value
        
        Args:
            key: Configuration key
            env: Environment name
            default: Default value if key not found
        
        Returns:
            Configuration value
        """
        env_config = self.get_env_config(env)
        return env_config.get(key, default)
    
    @property
    def base_url(self) -> str:
        """Get base URL for current environment"""
        return self.get('base_url')
    
    @property
    def timeout(self) -> int:
        """Get default timeout for current environment"""
        return self.get('timeout', default=10)
    
    @property
    def browser(self) -> str:
        """Get browser from environment variable or default"""
        return os.getenv('BROWSER', 'chrome').lower()
    
    @property
    def headless(self) -> bool:
        """Check if browser should run in headless mode"""
        return os.getenv('HEADLESS', 'false').lower() == 'true'
    
    @property
    def environment(self) -> str:
        """Get current environment name"""
        return os.getenv('ENV', 'dev')


# Singleton instance
config = Config()