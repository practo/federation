from federation_api.people.model import Person
from tests.factories.person_factory import PersonFactory


class TestPerson():
    def test_new(self):
        person = Person.new(name='name', email='a@b.com')
        assert person.name == 'name'
        assert person.email == 'a@b.com'


    def test_create(self):
        old_count = Person.count()
        person = Person.create(name='name')
        new_count = Person.count()
        assert not person.errors
        assert person.id
        assert new_count - old_count == 1


    def test_list(self):
        PersonFactory.create_batch(3)
        people = Person.list().all()
        assert len(people) == 3


    def test_first(self):
        PersonFactory.create_batch(3)
        person = Person.first()
        assert person.id == 1


    def test_last(self):
        PersonFactory.create_batch(3)
        person = Person.last()
        assert person.id == 3


    def test_list_with_deleted(self):
        PersonFactory.create_batch(3)
        Person.last().delete()

        people = Person.list().all()
        all_people = Person.list_with_deleted().all()
        assert len(people) == 2
        assert len(all_people) == 3


    def test_where(self):
        person = PersonFactory.create(name='name')

        people = Person.where(name='name')
        assert people.all()[0] == person
        assert people.count() == 1


    def test_find(self):
        person = PersonFactory.create()

        name_person = Person.find(1)
        assert name_person.id == person.id


    def test_find_by(self):
        person = PersonFactory.create(name='name')

        name_person = Person.find_by(name='name')
        assert name_person.id == person.id