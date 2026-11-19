# cac lop cau hinh moi truong (Dev, Test, Prod)
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY","fallback-low-security-key")
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'
    
class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL","sqlite:///dev.db")
    
class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory"

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    
    @classmethod
    def init_app(cls,app):
        assert cls.SECRET_KEY != "fallback-low-security-key", "Production SECRET_KEY must be secure!"
        
config ={
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production":ProductionConfig   
}
    
