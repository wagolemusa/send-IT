import os


class Config:
    """ Class to hold common configs for all classes """
    DEBUG = False
    SECRET_KEY = os.getenv('SECRET_KEY')
    TESTING = False


class ProductionConfig(Config):
    """ Class define variables for the production environment """
    DEBUG = False
    APP_ENV='production'


class DevelopmentConfig(Config):
    TESTING = True
    DATABASE_URI = "dbname='sendit', user='postgres', password='refuge', host='localhost'"
    APP_ENV='development'

class Testing(Config):
    TESTING = True
    DB_NAME = os.getenv('TEST_DB')
    APP_ENV='testing'


app_config = {
    'development': DevelopmentConfig,
    'testing': Testing,
    'production': ProductionConfig
}