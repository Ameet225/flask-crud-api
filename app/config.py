"""
Flask application configuration.

This module defines configuration classes for different environments
(development, testing, production). Each configuration class sets
specific parameters for the Flask application and SQLAlchemy ORM.
"""

import os


class Config:
    """
    Base configuration class with common settings for all environments.
    
    This class contains shared configuration parameters. Subclasses
    override specific settings for their respective environments.
    """
    
    # SQLAlchemy configuration
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JSON response configuration
    JSON_SORT_KEYS = False
    
    # Security: Strict mode for JSON responses
    JSON_STRICT = True


class DevelopmentConfig(Config):
    """
    Development environment configuration.
    
    Settings optimized for local development, including debug mode
    and detailed error reporting.
    """
    
    DEBUG = True
    TESTING = False
    
    # SQLite database for development
    # Database file will be created in the instance folder
    basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    instance_path = os.path.join(basedir, 'instance')
    os.makedirs(instance_path, exist_ok=True)
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(instance_path, "app.db")}'


class TestingConfig(Config):
    """
    Testing environment configuration.
    
    Settings optimized for running unit and integration tests,
    using an in-memory SQLite database for speed.
    """
    
    DEBUG = True
    TESTING = True
    
    # In-memory SQLite database for fast testing
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


class ProductionConfig(Config):
    """
    Production environment configuration.
    
    Settings optimized for production deployment.
    Database URI should be set via environment variable.
    """
    
    DEBUG = False
    TESTING = False
    
    # Production database URI should be set via environment variable
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'sqlite:///./instance/app.db'
    )


# Configuration dictionary for easy access
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
