class Config:
    DEBUG = True
    TESTING = False
    DATABASE_URI = ''


# Configurations for production
class ProductionConfig(Config):
    DEBUG = False
    DATABASE_URI = ''


# Configurations for development
class DevelopmentConfig(Config):
    pass


class Testing(Config):
    DEBUG = True
    TESTING = True


app_config = {
    'development': DevelopmentConfig,
    'testing': Testing,
    'production': ProductionConfig
}