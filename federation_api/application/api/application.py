import logging
from flask import make_response, jsonify
from config.db import db
from __init__ import application


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
