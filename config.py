import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    db_path = os.path.join(basedir, 'clog.db')


class ProdConfig(Config):
    pass


class DevConfig(Config):
    DEBUG = True


class TestConfig(Config):
    TESTING = True
    db_path = ':memory:'


def get_config(default='dev'):
    env = os.getenv('CLOG_ENV', default) or default
    return globals().get('{}Config'.format(env.title()))
