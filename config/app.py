from flask import Flask, make_response, jsonify
from environment import load_config
from db import db
from router import load_blueprints
from logger import init_logger
from config.initializers.errors import RequestErrorHandling


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    load_config(app)
    db.init_app(app)
    load_blueprints(app)
    init_logger(app)
    RequestErrorHandling(app)


    config = app.config
    ENV = config.get('ENVIORNMENT')
    if(ENV in ['DEVELOPMENT', 'TEST']):
        @app.route('/', methods=['GET'])
        def index():
            env = {}
            for configuration, value in config.iteritems():
                env[configuration] = str(value)
            return make_response(jsonify(env), 200)

    return app
