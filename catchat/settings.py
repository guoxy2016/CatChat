import os

BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Base:
    CATCHAT_MESSAGE_PER_PAGE = 30
    CATCHAT_ADMIN_EMAIL = os.getenv('ADMIN_EMAIL', 'admin@catchat.com')
    SECRET_KEY = 'secret-key'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class Development(Base):
    DEBUG = True
    SECRET_KEY = os.getenv('SECRET_KEY', 'development-key')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.getenv('DATABASE_URI', os.path.join(BASEDIR, 'data-dev.db'))


class Testing(Base):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False


class Production(Base):
    SECRET_KEY = os.getenv('SECRET_KEY', os.urandom(32))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.getenv('DATABASE_URI', os.path.join(BASEDIR, 'data.db'))


config = {
    'development': Development,
    'testing': Testing,
    'production': Production
}
