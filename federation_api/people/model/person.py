from federation_api.application.model import StarFleet
from config.db import db


class Person(StarFleet):
    __tablename__ = 'people'

    id = db.Column(db.Integer, nullable=False, primary_key=True)
    email = db.Column(db.String(length=50), nullable=True, unique=True,
                      index=True)
    phone = db.Column(db.String(length=20), nullable=True, unique=True,
                      index=True)
    account_id = db.Column(db.String(length=20), nullable=True, unique=True,
                           index=True)
    name = db.Column(db.String(length=50), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())
    updated_at = db.Column(db.DateTime, nullable=False, default=db.func.now(),
                           onupdate=db.func.now())
    deleted_at = db.Column(db.DateTime(), default=None, nullable=True)
