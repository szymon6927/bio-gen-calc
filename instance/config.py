from os import environ

SECRET_KEY = environ.get('SECRET_KEY', 'secret')

DB_USER = environ.get('DB_USER', 'root')
DB_PASSWORD = environ.get('DB_PASSWORD', '')
DB_NAME = environ.get('DB_NAME', 'gene_calc')
DB_HOST = environ.get('DB_HOST', 'localhost')

MYSQL_DATABASE = environ.get('MYSQL_DATABASE')
MYSQL_USER = environ.get('MYSQL_USER')
MYSQL_PASSWORD = environ.get('MYSQL_PASSWORD')

RECAPTCHA_PUBLIC_KEY = environ.get('RECAPTCHA_PUBLIC_KEY')
RECAPTCHA_PRIVATE_KEY = environ.get('RECAPTCHA_PRIVATE_KEY')

USE_DOCKER = int(environ.get('DOCKER', 0))

if USE_DOCKER == 1:
    SQLALCHEMY_DATABASE_URI = f'mysql://{MYSQL_USER}:{MYSQL_PASSWORD}@database/{MYSQL_DATABASE}'
else:
    SQLALCHEMY_DATABASE_URI = f'mysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'

# SQLALCHEMY_DATABASE_URI = 'mysql://m1259_admin_gene:576AaYaEL3Qqrc5H@mysql26.mydevil.net/m1259_gene_calc_test'
