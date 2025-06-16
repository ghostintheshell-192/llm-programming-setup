"""
Configuration settings for the example application.
"""

import os
from dataclasses import dataclass


@dataclass
class Config:
    """Application configuration."""
    DEBUG: bool = os.getenv('DEBUG', 'False').lower() == 'true'
    HOST: str = os.getenv('HOST', '0.0.0.0')
    PORT: int = int(os.getenv('PORT', 5000))
    DATABASE_URL: str = os.getenv('DATABASE_URL', 'sqlite:///app.db')
    
    # API Keys
    API_KEY: str = os.getenv('API_KEY', '')
    SECRET_KEY: str = os.getenv('SECRET_KEY', 'dev-secret-key')


# Global config instance
config = Config()