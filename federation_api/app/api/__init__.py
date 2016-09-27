from flask import Blueprint, make_response, jsonify

application = Blueprint('application', __name__)
people = Blueprint('people', __name__)

def set_instance(model, id):
        instance = model.find(id)
        if(not instance):
            raise NotFoundException(model=model.__name__, attribute='id', value=id)
        return instance


class NotFoundException(Exception):
    message = None

    def __init__(self, **config):
        try:
            self.message = make_response(jsonify(
                {
                    'status': '{0} with {1}={2} not found'.format(config['model'], config['attribute'], config['value'])
                }), 404)
            Exception.__init__(self)
        except KeyError as e:
            raise SyntaxError('{0} is missing'.format(e.message))

