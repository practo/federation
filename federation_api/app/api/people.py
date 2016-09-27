from flask import request, make_response, jsonify
from federation_api.app.api.__init__ import people, set_instance, \
    sanitized_parameters, permitted_parameters, \
    NotFoundException, MalformedRequestException, \
    UnpermittedParametersException
from federation_api.app.helper.__init__ import StarFleetHelper
from federation_api.app.model.person import Person


@people.route('', methods=['GET'])
def index():
    people = Person.all()
    attributes = ['name']

    return make_response(jsonify(
            StarFleetHelper.bulk_serialize_as_json(people, *attributes)
        ), 200)


@people.route('/<id>', methods=['GET'])
def show(id):
    try:
        person = set_instance(Person, id)
    except NotFoundException as e:
        return e.message
    attributes = ['name', 'created_at', 'updated_at']
    config = {'datetime_format': '%a %b %d %H:%M:%S %Y'}

    return make_response(jsonify(
            StarFleetHelper.serialize_as_json(person, *attributes, **config)
        ), 200)


@people.route('', methods=['POST'])
def create():
    required_attributes = ['name', 'email', 'account_id', 'phone']
    try:
        person = Person.create(
            **sanitized_parameters(Person, request.json, *required_attributes))
    except MalformedRequestException as e:
        return e.message
    if(person.errors):
        return make_response(jsonify(
            {
                'status': [error.message for error in person.errors]
            }), 422)
    attributes = ['name', 'created_at', 'updated_at']
    config = {'datetime_format': '%a %b %d %H:%M:%S %Y'}

    return make_response(jsonify(
            StarFleetHelper.serialize_as_json(person, *attributes, **config)
        ))


@people.route('/<id>', methods=['PUT'])
def update(id):
    update_attributes = ['name']
    try:
        person = set_instance(Person, id)
    except NotFoundException as e:
        return e.message
    try:
        person = person.update(
            **permitted_parameters(Person, request.json, *update_attributes))
    except UnpermittedParametersException as e:
        return e.message
    if(person.errors):
        return make_response(jsonify(
            {
                'status': [error.message for error in person.errors]
            }), 422)
    attributes = ['name', 'created_at', 'updated_at']
    config = {'datetime_format': '%a %b %d %H:%M:%S %Y'}

    return make_response(jsonify(
            StarFleetHelper.serialize_as_json(person, *attributes, **config)
        ))
