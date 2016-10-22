from flask import request
from federation_api.people.api.__init__ import people
from federation_api.application.api import StarFleets
from federation_api.application.helper import to_json
from federation_api.people.helper import PeopleHelper
from federation_api.people.model import Person


class People(StarFleets):
    @people.route('', methods=['GET'])
    @to_json
    def index():
        people = Person.list().all()
        attributes = ['name']
        config = {'root': True, 'root_name': 'people'}

        return PeopleHelper.bulk_serialize(people, *attributes, **config)

    @people.route('/<id>', methods=['GET'])
    @to_json
    def show(id):
        person = People.set_instance(Person, id)
        attributes = ['name', 'created_at', 'updated_at']
        config = {'datetime_format': '%a %b %d %H:%M:%S %Y'}

        return PeopleHelper.serialize(person, *attributes, **config)

    @people.route('', methods=['POST'])
    @to_json
    def create():
        required_attributes = ['name', 'email', 'account_id', 'phone']
        person = Person.create(
            **People.sanitized_parameters(Person, request.json,
                                          *required_attributes))
        People.process_instance(person)
        attributes = ['name', 'created_at', 'updated_at']
        config = {'datetime_format': '%a %b %d %H:%M:%S %Y'}

        return PeopleHelper.serialize(person, *attributes, **config), 201

    @people.route('/<id>', methods=['PUT'])
    @to_json
    def update(id):
        update_attributes = ['name']
        person = People.set_instance(Person, id)
        person = person.update(
            **People.permitted_parameters(Person, request.json,
                                          *update_attributes))
        People.process_instance(person)
        attributes = ['name', 'created_at', 'updated_at']
        config = {'datetime_format': '%a %b %d %H:%M:%S %Y'}

        return PeopleHelper.serialize(person, *attributes, **config)

    @people.route('/<id>', methods=['DELETE'])
    @to_json
    def delete():
        person = People.set_instance(Person, id)
        person = person.delete()

        return "Person with id='{0}' was successfully deleted".format(id), 202
