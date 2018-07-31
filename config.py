# config.py


class Config(object):
    """
    Common configurations
    """


class DevelopmentConfig(Config):
    """
    Development configurations
    """
    SECRET_KEY = 'p9Bv<3Eid9%$i01'
    DATABASE_FILE = 'sample_db.sqlite'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE_FILE
    DEBUG = True
    SQLALCHEMY_ECHO = True


class ProductionConfig(Config):
    """
    Production configurations
    """

    DEBUG = False


app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
