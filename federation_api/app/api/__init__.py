from flask import Blueprint, make_response, jsonify
from inflection import underscore

application = Blueprint('application', __name__)
people = Blueprint('people', __name__)


def set_instance(model, id):
    instance = model.find(id)
    if(not instance):
        raise NotFoundException(model=model.__name__, attribute='id', value=id)

    return instance


def droid_parameters(model, parameters, droid_key):
    if(droid_key not in parameters.keys()):
        raise MalformedRequestException(droid_key)

    return parameters[droid_key]


def sanitized_parameters(model, parameters, *droid_names):
    droid_key = underscore(model.__name__)
    model_parameters = droid_parameters(model, parameters, droid_key)
    sanitized_droid_names = {}
    missing_droid_names = []
    for droid_name in droid_names:
        try:
            sanitized_droid_names[droid_name] = model_parameters[droid_name]
        except KeyError:
            missing_droid_names.append('.'.join([droid_key, droid_name]))
    if(missing_droid_names):
        raise MalformedRequestException(missing_droid_names)

    return sanitized_droid_names


def permitted_parameters(model, parameters, *droid_names):
    droid_key = underscore(model.__name__)
    model_parameters = droid_parameters(model, parameters, droid_key)
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
        raise UnpermittedParametersException(unpermitted_droid_names)

    return permitted_droid_names


class NotFoundException(Exception):
    message = None

    def __init__(self, **config):
        try:
            self.message = make_response(jsonify(
                {
                    'status': ["{0} with {1}='{2}' not found"
                               .format(config['model'], config['attribute'],
                                       config['value'])]
                }), 404)
            Exception.__init__(self)
        except KeyError as e:
            raise SyntaxError('{0} is missing'.format(e.message))


class MalformedRequestException(Exception):
    message = None

    def __init__(self, keys):
        try:
            self.message = make_response(jsonify(
                {
                    'status': ["'{0}' key is missing".format(key)
                               for key in keys]
                }), 422)
            Exception.__init__(self)
        except KeyError as e:
            raise SyntaxError('{0} is missing'.format(e.message))


class UnpermittedParametersException(Exception):
    message = None

    def __init__(self, keys):
        try:
            self.message = make_response(jsonify(
                {
                    'status': ["'{0}' key cannot be updated"
                               .format(key) for key in keys]
                }), 422)
            Exception.__init__(self)
        except KeyError as e:
            raise SyntaxError('{0} is missing'.format(e.message))
