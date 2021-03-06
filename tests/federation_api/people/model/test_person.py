import pytest
from sqlalchemy.exc import InvalidRequestError
from config.db import db
from federation_api.people.model import Person
from tests.factories.person_factory import PersonFactory


class TestPerson():
    def test_new(self):
        person = Person.new(name='name', email='a@b.com')
        assert person.name == 'name'
        assert person.email == 'a@b.com'


    def test_save(self):
        person = PersonFactory.build()
        person.save()
        assert person.id is not None


    def test_create(self):
        old_count = Person.count()
        person = Person.create(name='name')
        new_count = Person.count()
        assert not person.errors
        assert person.id
        assert new_count - old_count == 1


    def test_list(self):
        PersonFactory.create_batch(3)
        db.session.commit()
        people = Person.list().all()
        assert len(people) == 3


    def test_first(self):
        PersonFactory.create_batch(3)
        db.session.commit()
        person = Person.first()
        assert person.id == 1


    def test_last(self):
        PersonFactory.create_batch(3)
        db.session.commit()
        person = Person.last()
        assert person.id == 3


    def test_list_with_deleted(self):
        PersonFactory.create_batch(3)
        db.session.commit()
        Person.last().delete()

        people = Person.list().all()
        all_people = Person.list_with_deleted().all()
        assert len(people) == 2
        assert len(all_people) == 3


    def test_where(self):
        person = PersonFactory.create(name='name')
        db.session.commit()
        people = Person.where(name='name')
        assert people.all()[0] == person
        assert people.count() == 1


    def test_find(self):
        person = PersonFactory.create()
        db.session.commit()
        name_person = Person.find(1)
        assert name_person.id == person.id


    def test_find_by(self):
        person = PersonFactory.create(name='name')
        db.session.commit()
        name_person = Person.find_by(name='name')
        assert name_person.id == person.id


    def test_destroy(self):
        person = PersonFactory.create()
        db.session.commit()
        person.destroy()
        destroy_person = Person.find(person.id)
        assert destroy_person is None


    def test_delete(self):
        person = PersonFactory.create()
        db.session.commit()
        person = person.delete()
        assert person.deleted_at is not None
