class Config:
    """
    Common configurations
    """
    COMPRESS_MIMETYPES = ['text/html', 'text/css', 'text/xml', 'application/json', 'application/javascript']
    COMPRESS_LEVEL = 8
    COMPRESS_MIN_SIZE = 500

    MINIFY_PAGE = True

    MAX_CONTENT_LENGTH = 4 * 1024 * 1024 # for file upload

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = "mail26.mydevil.net"
    MAIL_PORT = 465
    MAIL_USE_SSL = True


class DevelopmentConfig(Config):
    """
    Development configurations
    """
    DEBUG = True


class ProductionConfig(Config):
    """
    Production configurations
    """
    DEBUG = False


class TestingConfig(Config):
    """
    Testing configurations
    """
    TESTING = True
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Bcrypt algorithm hashing rounds (reduced for testing purposes only!)
    BCRYPT_LOG_ROUNDS = 4
    
    # Disable CSRF tokens in the Forms (only valid for testing purposes!)
    WTF_CSRF_ENABLED = False


app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}
