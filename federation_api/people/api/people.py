from flask import request, make_response, jsonify
from federation_api.people.api.__init__ import people
from federation_api.application.api import StarFleetAPI, \
    NotFoundException, RequestParametersException, UnprocessibleEntryException
from federation_api.application.helper import StarFleetHelper
from federation_api.people.model import Person


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
        person = StarFleetAPI.set_instance(Person, id)
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
            **StarFleetAPI.sanitized_parameters(Person, request.json,
                                                *required_attributes))
        StarFleetAPI.process_instance(person)
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
        person = StarFleetAPI.set_instance(Person, id)
        person = person.update(
            **StarFleetAPI.permitted_parameters(Person, request.json,
                                                *update_attributes))
        StarFleetAPI.process_instance(person)
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
        person = StarFleetAPI.set_instance(Person, id)
        person = person.delete()
    except (NotFoundException, UnprocessibleEntryException) as e:
        return e.message

    return make_response(jsonify(
        {
            'status': "Person with id='{0}' was successfully deleted"
                      .format(id)
        }), 202)
