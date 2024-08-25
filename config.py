import os, logging
from flask import Flask

class Config:
    ENV = os.environ.get('ENV') or 'development'
    SECRET_KEY = os.getenv('SECRET_KEY') or os.environ.get('SECRET_KEY') or os.urandom(32)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    DEBUG = (ENV == 'development')  # Enable debug mode only in development
    EMERGENCY_MODE = os.getenv('EMERGENCY_MODE') or os.environ.get('EMERGENCY_MODE') or False
    
    CLIENT_ORIGINS = os.getenv('CLIENT_ORIGINS') or os.environ.get('CLIENT_ORIGINS') or 'http://localhost:3000,http://localhost:5173'
    CLIENT_ORIGINS = [origin.strip() for origin in CLIENT_ORIGINS.split(',')]

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL') or "sqlite:///db.sqlite3"

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL_PROD')


# Map config based on environment
config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}

def configure_logging(app: Flask):
    if not app.logger.handlers:
        formatter = logging.Formatter("[%(asctime)s] ==> %(levelname)s in %(module)s: %(message)s")
        
        # Stream handler
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        app.logger.addHandler(stream_handler)
        
        app.logger.setLevel(logging.INFO)  # Set the desired logging level