import urllib
from flask import url_for
from flask_script import Manager, Server, Shell, Command
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


class Routes(Command):
    def run(self):
        output = []
        app = manager.app

        for rule in app.url_map.iter_rules():
            options = {}
            for arg in rule.arguments:
                options[arg] = "[{0}]".format(arg)

            methods = ','.join(rule.methods)
            # FIXME: Results in http://<host_name>:<host_port>/<blueprint_mount>/<endpoint>g
            url = url_for(rule.endpoint, **options)
            line = urllib.unquote("{:50s} {:20s} {}".format(rule.endpoint, methods,
                                                            url))
            output.append(line)

        for line in sorted(output):
            print(line)
manager.add_command('routes', Routes())


if __name__ == '__main__':
    manager.run()
