import os
from flask_environments import Environments


class CommonConfig(object):
    TESTING = False
    DEBUG = False
    CSRF_ENABLED = True
    SECRET_KEY = 'This is a good s3cr3t k3y'
    # DB
    SQLALCHEMY_DEBUG = DEBUG
    PYTHONPATH = os.getcwd()
    APPLICATION_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                    '..'))
    CONFIG_PATH = os.path.abspath(os.path.join(APPLICATION_ROOT, 'config',
                                               'config.yml'))
    # Newrelic
    ENABLE_NEWRELIC_MONITORING = False


class DevelopmentConfig(CommonConfig):
    DEBUG = True
    # DB
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/federation_development.db'
    # Newrelic
    ENABLE_NEWRELIC_MONITORING = True
    NEWRELIC_INI_PATH = os.path.abspath(os.path.join(
        CommonConfig.APPLICATION_ROOT, 'etc', 'newrelic.ini'))


class TestConfig(CommonConfig):
    TESTING = True
    # DB
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/federation_test.db'


class StagingConfig(CommonConfig):
    # DB
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/federation_staging.db'
    # Newrelic
    ENABLE_NEWRELIC_MONITORING = True
    NEWRELIC_INI_PATH = os.path.abspath(os.path.join(
        CommonConfig.APPLICATION_ROOT, 'etc', 'newrelic.ini'))


class LatestConfig(CommonConfig):
    # DB
    SQLALCHEMY_DATABASE_URI = ''
    # Newrelic
    ENABLE_NEWRELIC_MONITORING = True
    NEWRELIC_INI_PATH = os.path.abspath(os.path.join(
        '/etc/newrelic/newrelic.ini'))


class ProductionConfig(CommonConfig):
    # DB
    SQLALCHEMY_DATABASE_URI = ''
    # Newrelic
    ENABLE_NEWRELIC_MONITORING = True
    NEWRELIC_INI_PATH = os.path.abspath(os.path.join(
        '/etc/newrelic/newrelic.ini'))

env_config = {
    'TESTING': TestConfig,
    'DEVELOPMENT': DevelopmentConfig,
    'STAGING': StagingConfig,
    'LATEST': LatestConfig,
    'PRODUCTION': ProductionConfig
}


def load_config(app):
    env = Environments(app)
    config = app.config
    ENV = config.get('ENVIORNMENT')
    # http://stackoverflow.com/questions/33738467/how-do-i-know-if-i-can-disable-sqlalchemy-track-modifications/33790196#33790196
    config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    if(ENV in ['LATEST', 'PRODUCTION']):
        config.from_object(CommonConfig)
        env.from_yaml(config['CONFIG_PATH'])
        return app

    config.from_object(env_config.get(ENV))

    return app
