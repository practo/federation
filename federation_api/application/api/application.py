import logging
from flask import make_response, jsonify
from config import ENV, config, db
from __init__ import application

if(ENV in ['DEVELOPMENT', 'TEST']):
    @application.route('/', methods=['GET'])
    def index():
        env = {}
        for configuration, value in config.iteritems():
            env[configuration] = str(value)
        return make_response(jsonify(env), 200)


@application.route('/status', methods=['GET'])
def status():
    message = {'status': {}}
    status_code = 200
    # Check status of DB
    try:
        db.engine.table_names()
        message.get('status')['Database'] = 'Up'
    except Exception as e:
        logging.exception(e)
        message.get('status')['Database'] = 'Down'
        status_code = 500

    return make_response(jsonify(message), status_code)