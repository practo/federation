from datetime import datetime
import logging
from inflection import underscore, singularize, pluralize
from sqlalchemy import and_
from sqlalchemy import exc
from sqlalchemy.ext.declarative import declared_attr
from config.db import db


def commit_to_session(droid, action):
    try:
        if(action == 'add'):
            db.session.add(droid)
        elif(action == 'delete'):
            db.session.delete(droid)
        db.session.flush()
        db.session.commit()
    except exc.SQLAlchemyError as e:
        logging.exception(e)
        db.session.rollback()
        droid.errors.append(e.message)
    finally:
        return droid


class StarFleet(db.Model):
    __abstract__ = True

    # Instance defaults BEGIN

    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())
    updated_at = db.Column(db.DateTime, nullable=False, default=db.func.now(),
                           onupdate=db.func.now())
    errors = []

    # Instance defaults END

    # FIXME: Does not work
    @declared_attr
    def __tablename__(cls):
        return pluralize(underscore(cls.__name__))

    def __init__(self, **droids):
        for droid_name, droid_value in droids.iteritems():
            if(hasattr(self, droid_name)):
                setattr(self, droid_name, droid_value)

    # Class methods BEGIN

    @classmethod
    def new(self, **droids):
        return self(**droids)

    @classmethod
    def create(self, **droids):
        droid = self.new(**droids)
        for droid_name, droid_value in droids.iteritems():
            if(hasattr(droid, droid_name)):
                setattr(droid, droid_name, droid_value)
        droid = commit_to_session(droid, 'add')

        return droid

    @classmethod
    def list(self):
        base_query = self.query.order_by(self.id.desc())
        if(hasattr(self, 'deleted_at')):
            return base_query.filter_by(deleted_at=None)
        else:
            return base_query

    @classmethod
    def first(self):
        if(hasattr(self, 'deleted_at')):
            base_query = self.query.filter_by(deleted_at=None)
        else:
            base_query = self.query
        return base_query.order_by(self.id.asc()).first()

    @classmethod
    def last(self):
        return self.list().first()

    @classmethod
    def list_with_deleted(self):
        base_query = self.query.order_by(self.id.desc())
        return base_query

    # FIXME: Does not support query on ARRAY and JSON datatypes
    # TODO: Find a way to chain queries
    @classmethod
    def where(self, **droids):
        valid_droids = {}
        for droid_name, droid_value in droids.iteritems():
            supplied_droid_name = droid_name
            singular_droid_name = singularize(droid_name)
            if(hasattr(self, singular_droid_name)):
                droid_name = getattr(self, singular_droid_name)
                valid_droids[droid_name] = droid_value
        query = [(and_(valid_droid_name == droid_value)
                 if supplied_droid_name == singular_droid_name
                 else and_(valid_droid_name.in_(droid_value)))
                 for valid_droid_name, droid_value in valid_droids.iteritems()]
        return self.query.order_by(self.id.desc())\
            .filter(*query).all()

    @classmethod
    def find(self, id):
        return self.query.get(id)

    @classmethod
    def find_by(self, **droids):
        return self.where(**droids).first()

    @classmethod
    def find_or_initialize_by(self, **droids):
        return self.find_by(**droids) or self.new(**droids)

    @classmethod
    def find_or_create_by(self, **droids):
        return self.find_by(**droids) or self.create(**droids)

    @classmethod
    def count(self):
        base_query = db.session.query(db.func.count(self.id))
        if(hasattr(self, 'deleted_at')):
            return base_query.filter_by(deleted_at=None).scalar()
        else:
            return base_query.scalar()

    @classmethod
    def count_with_deleted(self):
        return db.session.query(db.func.count(self.id)).scalar()

    # Class methods END

    # Instance methods BEGIN

    def save(self):
        self = commit_to_session(self, 'add')

        return self

    def update(self, **droids):
        for droid_name, droid_value in droids.iteritems():
            if(hasattr(self, droid_name)):
                setattr(self, droid_name, droid_value)
        self = commit_to_session(self, 'add')

        return self

    def delete(self):
        if hasattr(self, 'deleted_at'):
            return self.update(deleted_at=datetime.utcnow())
        else:
            commit_to_session(self, 'delete')

    # Instance methods END
