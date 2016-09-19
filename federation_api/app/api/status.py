import logging
from flask import make_response, jsonify
from federation_api.app.api import application
from app import db


@application.route('/status', methods=['GET'])
def status():
    message = {'status': {}}
    status_code = 200
    # Check status of DB
    try:
        # Specfic to Postgres
        db.engine.table_names()
        message.get('status')['Database'] = 'Up'
    except Exception as e:
        logging.exception(e)
        message.get('status')['Database'] = 'Down'
        status_code = 500

    return make_response(jsonify(message), status_code)
