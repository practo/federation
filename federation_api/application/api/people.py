from flask import request, make_response, jsonify
from federation_api.app.api.__init__ import people
from federation_api.app.api.application import set_instance, \
    sanitized_parameters, permitted_parameters, process_instance, \
    NotFoundException, RequestParametersException, UnprocessibleEntryException
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
        process_instance(person)
    except (RequestParametersException, UnprocessibleEntryException) as e:
        return e.message

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
        person = person.update(
            **permitted_parameters(Person, request.json, *update_attributes))
        process_instance(person)
    except (NotFoundException, RequestParametersException,
            UnprocessibleEntryException) as e:
        return e.message

    attributes = ['name', 'created_at', 'updated_at']
    config = {'datetime_format': '%a %b %d %H:%M:%S %Y'}

    return make_response(jsonify(
            StarFleetHelper.serialize_as_json(person, *attributes, **config)
        ))


@people.route('/<id>', methods=['DELETE'])
def delete():
    try:
        person = set_instance(Person, id)
        person = person.delete()
    except (NotFoundException, UnprocessibleEntryException) as e:
        return e.message

    return make_response(jsonify(
        {
            'status': "Person with id='{0}' was successfully deleted"
                      .format(id)
        }), 202)
