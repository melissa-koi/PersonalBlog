import os

class Config:
    """
    General configuration class
    """
    SECRET_KEY ='jhfhlfhw'
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://koi:password@localhost/blog'
    SIMPLEMDE_JS_IIFE = True
    SIMPLEMDE_USE_CDN = True
    UPLOADED_PHOTOS_DEST ='app/static/photos'
    #
    # #  email configurations
    # MAIL_SERVER = 'smtp.googlemail.com'
    # MAIL_PORT = 587
    # MAIL_USE_TLS = True
    # MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    # MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    #

class ProdConfig(Config):
    """
    Production configuration class
    """
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")


class DevConfig(Config):
    """
    Development configuration class
    """
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://koi:password@localhost/blog'

class TestConfig(Config):
    '''
    Testing configuration child class
    Args:
        Config: The parent configuration class with General configuration settings
    '''
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://koi:password@localhost/blog'

config_options = {
    'production': ProdConfig,
    'development': DevConfig,
    'test':TestConfig
}
