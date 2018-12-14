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
    DATABASE_URI = "connection = psycopg2.connect(dbname='d92a0rb0j8rphh', user='gaijmyignhvtkw', password='7e0acadc7013645d81437d922b7030782cdee4006cadf7f54501aa291b29d3e6', host='ec2-23-21-65-173.compute-1.amazonaws.com'"
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