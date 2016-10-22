import logging
from config.db import db
from __init__ import application
from federation_api.application.helper import to_json


@application.route('/status', methods=['GET'])
@to_json
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

    return message, status_code
