import logging


def init_logger(app):
    app.logger.setLevel(logging.INFO)
    app.logger.addHandler(logging.StreamHandler())
