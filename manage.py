from flask_script import Manager, Server, Shell
from config.app import create_app
from config.db import db
from config.initializers.newrelic_monitoring import NewrelicMonitoring
from federation_api.people.model import Person

manager = Manager(create_app)

server = Server(host='0.0.0.0', port=1786)
NewrelicMonitoring(manager.app())
manager.add_command('runserver', server)


def _make_context():
    models = [Person]
    models = {model.__name__: model for model in models}

    return dict(app=create_app(), db=db, **models)
manager.add_command('shell', Shell(make_context=_make_context))

if __name__ == '__main__':
    manager.run()

