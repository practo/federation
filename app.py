import sys
import getopt
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
ENV = config.get('ENVIORNMENT')
if ENV == 'TEST':
    app.config.from_object(TestConfig)
elif ENV == 'DEVELOPMENT':
    app.config.from_object(DevelopmentConfig)
elif ENV == 'STAGING':
    app.config.from_object(StagingConfig)
elif ENV == 'LATEST':
    app.config.from_object(LatestConfig)
elif ENV == 'PRODUCTION':
    app.config.from_object(ProductionConfig)
else:
    # TODO: ENV not set
    pass


if(ENV in ['LATEST', 'PRODUCTION']):
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
db = SQLAlchemy(app)

from config.routes import blueprints
for blueprint_name, blueprint_url_prefix in blueprints:
    app.register_blueprint(blueprint_name, url_prefix=blueprint_url_prefix)

# New relic monitoring
def _init_newrelic_monitoring():
    if config.get('ENABLE_NEWRELIC_MONITORING', False):
        newrelic_ini = config.get('NEWRELIC_INI_PATH', False)
        if(newrelic_ini):
            from newrelic import agent as newrelic_agent
            newrelic_agent.initialize(newrelic_ini, ENV.lower())
            app.wsgi_app = newrelic_agent.WSGIApplicationWrapper(app.wsgi_app)


def command_help():
    print('Usage: app.py [options]\n')
    print('Options:')
    print('\t-h, --host    Host binding IP[0.0.0.0]')
    print('\t-p, --port    Port[1786]')
    print('\t-h, --help    Help')
    sys.exit(1)


if __name__ == '__main__':
    options, remainder = getopt.getopt(sys.argv[1:],
                                       'h:p:h', ['host=', 'port=', 'help'])
    host = '0.0.0.0'
    port = 1786
    for o, p in options:
        if o in ['-h', '--host']:
            host = p
        elif o in ['-p', '--port']:
            port = int(p)
        else:
            command_help()

    _init_newrelic_monitoring()
    app.run(host=host, port=port)
