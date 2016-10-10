import pytest

from config import app
from monkeyApp.extensions import db as _db


@pytest.fixture()
def app():
    return app


@pytest.fixture(scope='function', autouse=True)
def db(app, request):
    _db.drop_all()
    _db.create_all()
    return _db