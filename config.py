# config.py


class Config(object):
    """
    Common configurations
    """
    MAX_CONTENT_LENGTH = 4 * 1024 * 1024
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = "mail26.mydevil.net"
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MINIFY_PAGE = True
    WHOOSH_BASE = 'whoosh'


class DevelopmentConfig(Config):
    """
    Development configurations
    """
    DEBUG = True


class ProductionConfig(Config):
    """
    Production configurations
    """
    COMPRESS_MIMETYPES = ['text/html', 'text/css', 'text/xml', 'application/json', 'application/javascript']
    COMPRESS_LEVEL = 6
    COMPRESS_MIN_SIZE = 500
    DEBUG = False


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
