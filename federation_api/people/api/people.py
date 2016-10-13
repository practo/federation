from flask import request, make_response, jsonify
from federation_api.people.api.__init__ import people
from federation_api.application.api import StarFleets
from federation_api.application.helper import StarFleetsHelper
from federation_api.people.model import Person


@people.route('', methods=['GET'])
def index():
    people = Person.all()
    attributes = ['name']

    return make_response(jsonify(
            StarFleetsHelper.bulk_serialize_as_json(people, *attributes)
        ), 200)


@people.route('/<id>', methods=['GET'])
def show(id):
    person = StarFleets.set_instance(Person, id)
    attributes = ['name', 'created_at', 'updated_at']
    config = {'datetime_format': '%a %b %d %H:%M:%S %Y'}

    return make_response(jsonify(
            StarFleetsHelper.serialize_as_json(person, *attributes, **config)
        ), 200)


@people.route('', methods=['POST'])
def create():
    required_attributes = ['name', 'email', 'account_id', 'phone']
    person = Person.create(
        **StarFleets.sanitized_parameters(Person, request.json,
                                          *required_attributes))
    StarFleets.process_instance(person)
    attributes = ['name', 'created_at', 'updated_at']
    config = {'datetime_format': '%a %b %d %H:%M:%S %Y'}

    return make_response(jsonify(
            StarFleetsHelper.serialize_as_json(person, *attributes, **config)
        ))


@people.route('/<id>', methods=['PUT'])
def update(id):
    update_attributes = ['name']
    person = StarFleets.set_instance(Person, id)
    person = person.update(
        **StarFleets.permitted_parameters(Person, request.json,
                                          *update_attributes))
    StarFleets.process_instance(person)
    attributes = ['name', 'created_at', 'updated_at']
    config = {'datetime_format': '%a %b %d %H:%M:%S %Y'}

    return make_response(jsonify(
            StarFleetsHelper.serialize_as_json(person, *attributes, **config)
        ))


@people.route('/<id>', methods=['DELETE'])
def delete():
    person = StarFleets.set_instance(Person, id)
    person = person.delete()

    return make_response(jsonify(
        {
            'status': "Person with id='{0}' was successfully deleted"
                      .format(id)
        }), 202)
