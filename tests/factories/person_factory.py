import random
from datetime import datetime
import factory
from tests.factories import faker
from faker import Factory
from config.db import db
from federation_api.people.model import Person


class PersonFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Person
        sqlalchemy_session = db.session

    email = factory.LazyAttribute(lambda x: faker.email())
    phone = factory.LazyAttribute(lambda x: faker.phone_number())
    account_id = factory.LazyAttribute(lambda x: random.randint(1000, 9999))
    name = factory.LazyAttribute(lambda x: faker.name())
