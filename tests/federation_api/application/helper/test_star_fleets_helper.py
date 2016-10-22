import pytest
from federation_api.application.helper.star_fleets_helper import StarFleetsHelper
from federation_api.people.model import Person
from tests.factories.person_factory import PersonFactory

class TestStarFleetsHelper():
    class TestSerialize():
        def test_none_object_without_root(self):
            with pytest.raises(KeyError):
                StarFleetsHelper.serialize(None, 'id')


        def test_none_object_with_root_error(self):
            with pytest.raises(KeyError):
                StarFleetsHelper.serialize(None, 'id', root=True)


        def test_none_object_with_root(self):
            serialized = StarFleetsHelper.serialize(
                None, 'id', root=True, root_name='thing')
            assert serialized == {'thing': {}}


        def test_none_keys_with_root(self):
            person = PersonFactory.create()
            serialized = StarFleetsHelper.serialize(person, None,
                                                            root=True)
            assert serialized == {'person': {}}


        def test_none_keys_without_root(self):
            person = PersonFactory.create()
            serialized = StarFleetsHelper.serialize(person, None,
                                                            root=False,
                                                            root_name='thing')
            assert serialized == {}


        def test_with_root_implicit(self):
            person = PersonFactory.create()
            serialized = StarFleetsHelper.serialize(person, 'name')
            assert serialized == {'person': {'name': person.name}}


        def test_with_root_explicit(self):
            person = PersonFactory.create()
            serialized = StarFleetsHelper.serialize(person, 'name',
                                                            root_name='thing')
            assert serialized == {'thing': {'name': person.name}}


        def test_without_root(self):
            person = PersonFactory.create()
            serialized = StarFleetsHelper.serialize(person, 'name',
                                                            root=False)
            assert serialized == {'name': person.name}


        def test_for_datetime(self):
            person = PersonFactory.create()
            serialized = StarFleetsHelper.serialize(person, 'name', 'created_at')
            assert serialized == {'person': {'name': person.name,
                                             'created_at': person.created_at}}


        def test_for_datetime_format(self):
            person = PersonFactory.create()
            serialized = StarFleetsHelper.serialize(person, 'name', 'created_at',
                                                            datetime_format='%s')
            assert serialized == {'person': {'name': person.name,
                                             'created_at': person.created_at.strftime('%s')}}


    class TestBulkSerialize():
        def test_none_object_without_root(self):
            with pytest.raises(KeyError):
                StarFleetsHelper.bulk_serialize(None, 'id')


        def test_none_object_with_root(self):
            with pytest.raises(KeyError):
                StarFleetsHelper.bulk_serialize(None, None, root=True)


        def test_none_object_with_root(self):
            serialized = StarFleetsHelper.bulk_serialize(
                None, 'id', root=True, root_name='thing')
            assert serialized == {'thing': [], 'total': 0}


        def test_none_keys_with_root(self):
            people = PersonFactory.create_batch(3)
            serialized = StarFleetsHelper.bulk_serialize(people, None,
                                                                 root=True)
            assert serialized == {'people': [{}, {}, {}], 'total': 3}


        def test_none_keys_without_root(self):
            people = PersonFactory.create_batch(3)
            serialized = StarFleetsHelper.bulk_serialize(people, None,
                                                                 root=False)
            assert serialized == [{}, {}, {}]


        def test_with_root_implicit(self):
            people = PersonFactory.create_batch(3)
            people = Person.list().all()
            serialized = StarFleetsHelper.bulk_serialize(people, 'name')
            assert serialized == {'people': [{'name': people[0].name},
                                             {'name': people[1].name},
                                             {'name': people[2].name}],
                                  'total': 3}


        def test_with_root_explicit(self):
            people = PersonFactory.create_batch(3)
            people = Person.list().all()
            serialized = StarFleetsHelper.bulk_serialize(people, 'name',
                                                                 root_name='thing')
            assert serialized == {'thing': [{'name': people[0].name},
                                            {'name': people[1].name},
                                            {'name': people[2].name}],
                                  'total': 3}


        def test_without_root(self):
            people = PersonFactory.create_batch(3)
            people = Person.list().all()
            serialized = StarFleetsHelper.bulk_serialize(people, 'name',
                                                                 root=False)
            assert serialized == [{'name': people[0].name},
                                  {'name': people[1].name},
                                  {'name': people[2].name}]
