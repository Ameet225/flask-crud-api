"""
Flask application factory.

This module creates and configures the Flask application using the
application factory pattern, enabling flexible initialization and
testing of the application.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Initialize SQLAlchemy ORM instance
db = SQLAlchemy()


def create_app(config_name='development'):
    """
    Application factory function.
    
    Creates and configures a Flask application instance with the
    specified configuration. This pattern allows for flexible app
    instantiation across different environments (development, testing, production).
    
    Args:
        config_name (str): Name of the configuration to use.
                          Options: 'development', 'testing', 'production'
    
    Returns:
        Flask: Configured Flask application instance
    """
    # Create Flask application instance
    app = Flask(__name__)
    
    # Import configuration dynamically
    from app.config import config
    app.config.from_object(config[config_name])
    
    # Initialize database with app
    db.init_app(app)
    
    # Register blueprints
    from app.routes import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # Error handlers are registered in routes module
    
    # Create database tables within application context
    with app.app_context():
        db.create_all()
    
    return app
