import os


class CommonConfig(object):
    PYTHONPATH = os.getcwd()
    ROOT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    CONFIG_PATH = os.path.abspath(os.path.join(ROOT_PATH, 'config', 'config.yml'))


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
