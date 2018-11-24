class Config:
    """
    Common configurations
    """
    MAX_CONTENT_LENGTH = 4 * 1024 * 1024
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = "mail26.mydevil.net"
    MAIL_PORT = 465
    MAIL_USE_SSL = True


class DevelopmentConfig(Config):
    """
    Development configurations
    """
    DEBUG = True
    MINIFY_PAGE = True


class ProductionConfig(Config):
    """
    Production configurations
    """
    COMPRESS_MIMETYPES = ['text/html', 'text/css', 'text/xml', 'application/json', 'application/javascript']
    COMPRESS_LEVEL = 6
    COMPRESS_MIN_SIZE = 500
    MINIFY_PAGE = True
    DEBUG = False


class TestingConfig(Config):
    """
    Testing configurations
    """
    TESTING = True
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # Bcrypt algorithm hashing rounds (reduced for testing purposes only!)
    BCRYPT_LOG_ROUNDS = 4
    # Disable CSRF tokens in the Forms (only valid for testing purposes!)
    WTF_CSRF_ENABLED = False


app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}
