"""
Application entry point.

This module serves as the entry point for running the Flask application.
It creates the application instance using the factory pattern and starts
the development server or allows WSGI servers (Gunicorn, uWSGI) to import
the app instance for production deployment.

Usage:
    Development:
        python run.py
    
    Production (Gunicorn):
        gunicorn -w 4 -b 0.0.0.0:5000 run:app
"""

import os
from app import create_app

# Determine configuration environment
config_env = os.getenv('FLASK_ENV', 'development')

# Create application instance
app = create_app(config_name=config_env)


if __name__ == '__main__':
    """
    Run the Flask application in development mode.
    
    This block only executes when run.py is executed directly.
    In production, WSGI servers import the 'app' object directly.
    """
    # Get port from environment or use default
    port = int(os.getenv('FLASK_PORT', 5000))
    
    # Get host from environment or use default
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    
    # Run the application
    app.run(
        host=host,
        port=port,
        debug=(config_env == 'development'),
        use_reloader=(config_env == 'development')
    )
