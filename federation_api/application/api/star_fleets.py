from inflection import underscore
from flask import make_response, jsonify
from config import app


class StarFleets():
    @classmethod
    def set_instance(self, model, id):
        instance = model.find(id)
        if(not instance):
            raise NotFoundException(model=model.__name__, attribute='id',
                                    value=id)

        return instance

    @classmethod
    def droid_parameters(self, model, parameters, droid_key):
        if(droid_key not in parameters.keys()):
            raise RequestParametersException('is missing', droid_key)

        return parameters[droid_key]

    @classmethod
    def sanitized_parameters(self, model, parameters, *droid_names):
        droid_key = underscore(model.__name__)
        model_parameters = self.droid_parameters(model, parameters, droid_key)
        sanitized_droid_names = {}
        missing_droid_names = []
        for droid_name in droid_names:
            try:
                sanitized_droid_names[droid_name] = \
                    model_parameters[droid_name]
            except KeyError:
                missing_droid_names.append('.'.join([droid_key, droid_name]))
        if(missing_droid_names):
            raise RequestParametersException('is missing',
                                             *missing_droid_names)

        return sanitized_droid_names

    @classmethod
    def permitted_parameters(self, model, parameters, *droid_names):
        droid_key = underscore(model.__name__)
        model_parameters = self.droid_parameters(model, parameters, droid_key)
        permitted_droid_names = {}
        unpermitted_droid_names = []
        for droid_name in droid_names:
            parameter = model_parameters.get(droid_name, False)
            if(parameter):
                permitted_droid_names[droid_name] = parameter
        unpermitted_droid_names = ['.'.join([droid_key, key])
                                   for key in model_parameters.keys()
                                   if key not in droid_names]
        if(unpermitted_droid_names):
            raise RequestParametersException('cannot be updated',
                                             *unpermitted_droid_names)

        return permitted_droid_names

    @classmethod
    def process_instance(self, droid):
        if(droid.errors):
            raise UnprocessibleEntryException(droid.errors)


class NotFoundException(Exception):
    def __init__(self, **config):
        Exception.__init__(self)
        try:
            self.message = make_response(jsonify(
                {
                    'status': ["{0} with {1}='{2}' not found"
                               .format(config['model'], config['attribute'],
                                       config['value'])]
                }), 404)
        except KeyError as e:
            raise SyntaxError('{0} is missing'.format(e.message))


class RequestParametersException(Exception):
    def __init__(self, message, *parameter_keys):
        Exception.__init__(self)
        try:
            self.message = make_response(jsonify(
                {
                    'status': ["'{0}' key {1}".format(parameter_key, message)
                               for parameter_key in parameter_keys]
                }), 422)
        except KeyError as e:
            raise SyntaxError('{0} is missing'.format(e.message))


class UnprocessibleEntryException(Exception):
    def __init__(self, errors):
        Exception.__init__(self)
        self.message = make_response(jsonify(
            {
                'status': [error.message for error in errors]
            }), 422)


@app.errorhandler(NotFoundException)
@app.errorhandler(RequestParametersException)
@app.errorhandler(UnprocessibleEntryException)
def handle_error(error):
    return error.message
