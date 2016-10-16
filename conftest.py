import pytest
from config.app import create_app
from config.initializers.errors import RequestErrorHandling
from config.db import db as _db


@pytest.fixture()
def app():
    app = create_app()

    RequestErrorHandling(app)
    # Router has to be imported at last as it in turns loads the application code
    with app.app_context():
        from config.router import load_blueprints
        load_blueprints(app)

    return app


@pytest.fixture(scope='function', autouse=True)
def db(app, request):
    _db.drop_all()
    _db.create_all()
    return _db
