import logging
from flask import make_response, jsonify
from federation_api.app.api import application
from app import db, ENV

if(ENV in ['latest', 'production']):
    @application.errorhandler(Exception)
    def generic(error):
        response = make_response(Exception, 500)
        response.mimetype = 'text/plain'
        return response


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
