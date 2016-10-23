import json
import pytest
from flask import url_for
from config.db import db
from tests.factories.person_factory import PersonFactory
from federation_api.people.helper import PeopleHelper
from federation_api.people.model import Person


@pytest.mark.usefixtures('client_class')
class TestPeople():
    def test_index(self):
        people = PersonFactory.create_batch(3)
        db.session.commit()
        response = self.client.get(url_for('people.index'))
        assert response.status_code == 200
        assert response.json == {
            'people': [
                {'name': people[2].name, 'updated_at': people[2].updated_at.strftime('%s')},
                {'name': people[1].name, 'updated_at': people[1].updated_at.strftime('%s')},
                {'name': people[0].name, 'updated_at': people[0].updated_at.strftime('%s')}
            ],
            'total': 3
        }


    def test_404(self):
        response = self.client.get(url_for('people.show', id=1))
        assert response.status_code == 404
        assert response.json == {
            'error': ["Person with id='1' not found"]
        }


    def test_show(self):
        person = PersonFactory.create()
        db.session.commit()
        response = self.client.get(url_for('people.show', id=person.id))
        assert response.status_code == 200
        assert response.json == {
            'person': {
                'name': person.name,
                'created_at': person.created_at.strftime('%a %b %d %H:%M:%S %Y'),
                'updated_at': person.updated_at.strftime('%a %b %d %H:%M:%S %Y')
            }
        }


    def test_create_failure(self):
        person = PersonFactory.build()
        person_data = PeopleHelper.serialize(person, None)
        old_count = Person.count()
        response = self.client.post(url_for('people.create'), data=json.dumps(person_data),
                                    content_type='application/json')
        new_count = Person.count()
        assert new_count == old_count
        assert response.status_code == 422
        assert response.json == {
            'error': [
                "'person.name' key is missing",
                "'person.email' key is missing",
                "'person.account_id' key is missing",
                "'person.phone' key is missing"
            ]
        }


    def test_create(self):
        person = PersonFactory.build()
        person_data = PeopleHelper.serialize(person, *['name', 'email', 'phone', 'account_id'])
        old_count = Person.count()
        response = self.client.post(url_for('people.create'), data=json.dumps(person_data),
                                    content_type='application/json')
        new_count = Person.count()
        person = Person.last()
        assert new_count == old_count + 1
        assert response.status_code == 201
        assert response.json == {
            'person': {
                'name': person.name,
                'created_at': person.created_at.strftime('%a %b %d %H:%M:%S %Y'),
                'updated_at': person.updated_at.strftime('%a %b %d %H:%M:%S %Y')
            }
        }


    def test_update_failure(self):
        person = PersonFactory.create()
        db.session.commit()
        response = self.client.put(url_for('people.update', id=person.id),
                                   data=json.dumps({'person': {'account_id': 'account_id'}}), content_type='application/json')
        assert response.status_code == 422
        assert response.json == {
            'error': ["'person.account_id' key cannot be updated"]
        }


    def test_update(self):
        person = PersonFactory.create()
        db.session.commit()
        response = self.client.put(url_for('people.update', id=person.id),
                                   data=json.dumps({'person': {'name': 'name'}}), content_type='application/json')
        assert response.status_code == 200
        assert response.json == {
            'person': {
                'name': 'name',
                'created_at': person.created_at.strftime('%a %b %d %H:%M:%S %Y'),
                'updated_at': person.updated_at.strftime('%a %b %d %H:%M:%S %Y')
            }
        }


    def test_delete(self):
        person = PersonFactory.create()
        db.session.commit()
        response = self.client.delete(url_for('people.delete', id=person.id))
        assert response.status_code == 202
        assert response.json == {
            "status": "Person with id=\'1\' was successfully deleted"
        }
