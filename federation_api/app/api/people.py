from flask import current_app, make_response, jsonify
from federation_api.app.api.__init__ import NotFoundException, set_instance, \
    people
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
    pass

