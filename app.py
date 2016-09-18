import logging
from flask import Flask, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_environments import Environments
from config.environments import CommonConfig, DevelopmentConfig, TestConfig, \
    StagingConfig, LatestConfig, ProductionConfig


app = Flask(__name__, instance_relative_config=True)
config = app.config

config.from_object(CommonConfig)
# TODO: Why is this used and find a better way to set this
config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
env = Environments(app)
env.from_yaml(config['CONFIG_PATH'])
ENV = config.get('ENV')
if ENV == 'test':
    app.config.from_object(TestConfig)
elif ENV == 'development':
    app.config.from_object(DevelopmentConfig)
elif ENV == 'staging':
    app.config.from_object(StagingConfig)
elif ENV == 'latest':
    app.config.from_object(LatestConfig)
elif ENV == 'production':
    app.config.from_object(ProductionConfig)
else:
    # TODO: ENV not set
    pass


if(ENV in ['latest', 'production']):
    @app.errorhandler(Exception)
    def generic(error):
        response = make_response(Exception, 500)
        response.mimetype = 'text/plain'
        return response

app.logger.setLevel(logging.INFO)
app.logger.addHandler(logging.StreamHandler())


# TODO: Log DB queries to logger at DEBUG level
# from sqlalchemy.dialects import postgresql
# q = ...
# logging.debug(str(q.statement.compile(dialect=postgresql.dialect())))
# FIXME: Remove all instances of db.session.close()
# Flask-SQLAlchemy already binds a session lifecycle to a request scope
db = SQLAlchemy(app)

import federation_api
from config.routes import blueprints
for blueprint_name, blueprint_url_prefix in blueprints:
    app.register_blueprint(blueprint_name, url_prefix=blueprint_url_prefix)

import sys
import getopt


def command_help():
    print 'Usage: app.py [options]\n'
    print 'Options:'
    print '\t-h, --host    Host binding IP[0.0.0.0]'
    print '\t-p, --port    Port[8000]'
    print '\t-h, --help    Help'
    sys.exit(1)


if __name__ == '__main__':
    options, remainder = getopt.getopt(sys.argv[1:],
                                       'h:p:h', ['host=', 'port=', 'help'])
    host = '0.0.0.0'
    port = 8000
    for o, p in options:
        if o in ['-h', '--host']:
            host = p
        elif o in ['-p', '--port']:
            port = int(p)
        else:
            command_help()

    app.run(host=host, port=port)
