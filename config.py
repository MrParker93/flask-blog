import os
from pathlib import Path
from dotenv import load_dotenv


# Set path to env file
env_var = Path(".") / ".env"
load_dotenv(dotenv_path=env_var)


class Config:
    """Base configuration"""

    TESTING = False
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    """Production configuration"""

    FLASK_ENV = "production"


class DevelopmentConfig(Config):
    """Development configuration"""

    FLASK_ENV = "development"
    DATABASE = "blog.db"
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_RECORD_QUERIES = True
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI") + DATABASE


class TestingConfig(Config):
    """Testing configuration"""

    TESTING = True
    DATABASE = "test.db"
    FLASK_ENV = "testing"
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI") + DATABASE
