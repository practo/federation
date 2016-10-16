import os
from flask_environments import Environments


class CommonConfig(object):
    PYTHONPATH = os.getcwd()
    APPLICATION_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                    '..'))
    CONFIG_PATH = os.path.abspath(os.path.join(APPLICATION_ROOT, 'config',
                                               'config.yml'))
    NEWRELIC_INI_PATH = os.path.abspath(os.path.join(APPLICATION_ROOT, 'etc',
                                                     'newrelic.ini'))


class DevelopmentConfig():
    pass


class TestConfig():
    pass


class StagingConfig():
    pass


class LatestConfig():
    pass


class ProductionConfig():
    pass


def load_config(app):
    env = Environments(app)
    config = app.config
    # http://stackoverflow.com/questions/33738467/how-do-i-know-if-i-can-disable-sqlalchemy-track-modifications/33790196#33790196
    config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    config.from_object(CommonConfig)
    env.from_yaml(config['CONFIG_PATH'])

    ENV = config.get('ENVIORNMENT')
    if ENV == 'TEST':
        config.from_object(TestConfig)
    elif ENV == 'DEVELOPMENT':
        config.from_object(DevelopmentConfig)
    elif ENV == 'STAGING':
        config.from_object(StagingConfig)
    elif ENV == 'LATEST':
        config.from_object(LatestConfig)
    elif ENV == 'PRODUCTION':
        config.from_object(ProductionConfig)
    else:
        # TODO: ENV not set
        pass

    return app
