from federation_api.application.api.__init__ import application
from federation_api.people.api.__init__ import people

blueprints = [
    [application, ''],
    [people, '/people']
]


def load_blueprints(app):
    for blueprint_name, blueprint_url_prefix in blueprints:
            app.register_blueprint(blueprint_name,
                                   url_prefix=blueprint_url_prefix)
