from federation_api.app.model import StarFleet
from app import db

class Person(StarFleet, db.Model):
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    email = db.Column(db.String(length=128), nullable=True, unique=True,
                                index=True)
    phone = db.Column(db.String(length=128), nullable=True, unique=True,
                                index=True)
    account_id = db.Column(db.String(length=128), nullable=True, unique=True,
                                     index=True)
    name = db.Column(db.String(length=128), nullable=True)