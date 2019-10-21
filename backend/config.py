import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    TESTING = False

    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') or 'postgresql://localhost:5432/coveapi_test'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
    JWT_IDENTITY_CLAIM = 'sub'

    # NO_MAIL - master variable to not send out mail
    # For use in test enviornments
    NO_MAIL = os.environ.get('NO_MAIL') == 'True' or False
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_DEFAULT_SENDER = 'cove@thecvf.com'

    BASE_URL = os.environ.get('BASE_URL') or 'http://localhost:8080/'
    NOTIFY_ADMIN_EMAIL = 'cove@thecvf.com'

    ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL')
