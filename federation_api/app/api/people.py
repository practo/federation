from flask import make_response, jsonify
from federation_api.app.api.__init__ import people
from federation_api.app.helper.__init__ import StarFleetHelper
from federation_api.app.model.person import Person


@people.route('/', methods=['GET'])
def index():
    people = Person.all()
    attributes = ['name']
    return make_response(jsonify(
            StarFleetHelper.bulk_serialize_as_json(people, *attributes)
        ), 200)
