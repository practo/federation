from flask import make_response, jsonify


class RequestErrorHandling():
    def __init__(self, app):
        @app.errorhandler(NotFoundException)
        @app.errorhandler(ParametersException)
        @app.errorhandler(UnprocessibleEntryException)
        def return_response(error):
            return error.message


class NotFoundException(Exception):
    def __init__(self, **config):
        Exception.__init__(self)
        try:
            self.message = make_response(jsonify(
                {
                    'error': ["{0} with {1}='{2}' not found"
                              .format(config['model'], config['attribute'],
                                      config['value'])]
                }), 404)
        except KeyError as e:
            raise SyntaxError('{0} is missing'.format(e.message))


class ParametersException(Exception):
    def __init__(self, message=None, *parameter_keys):
        Exception.__init__(self)
        if(parameter_keys):
            self.message = make_response(jsonify(
                {
                    'error': ["'{0}' key {1}".format(parameter_key, message)
                              for parameter_key in parameter_keys]
                }), 422)
        else:
            raise SyntaxError('No parameters provided')


class UnprocessibleEntryException(Exception):
    def __init__(self, errors=[]):
        Exception.__init__(self)
        self.message = make_response(jsonify(
            {
                'error': errors
            }), 422)
