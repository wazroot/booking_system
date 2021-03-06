import os

class Config:
    
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_ERROR_MESSAGE_KEY = 'message'
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
   
class DevelopmentConfig(Config):
    
    DEBUG = True
    SECRET_KEY = 'super-secret-key'
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://wazroot:19Piippolanvaari88@localhost/projekti'


class ProductionConfig(Config):
    
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

class StagingConfig(Config):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

