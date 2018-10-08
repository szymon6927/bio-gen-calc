# config.py


class Config(object):
    """
    Common configurations
    """
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    MAIL_SERVER = "mail26.mydevil.net"
    MAIL_PORT = 465
    MAIL_USE_SSL = True


class DevelopmentConfig(Config):
    """
    Development configurations
    """
    SQLALCHEMY_ECHO = True
    DEBUG = True
    MINIFY_PAGE = True


class ProductionConfig(Config):
    """
    Production configurations
    """
    COMPRESS_MIMETYPES = ['text/html', 'text/css', 'text/xml', 'application/json', 'application/javascript']
    COMPRESS_LEVEL = 6
    COMPRESS_MIN_SIZE = 500
    SQLALCHEMY_ECHO = False
    DEBUG = False
    MINIFY_PAGE = True


class TestingConfig(Config):
    """
    Testing configurations
    """
    TESTING = True
    SQLALCHEMY_ECHO = True


app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}
