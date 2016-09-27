import os


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
