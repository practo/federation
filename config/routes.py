from federation_api.app.api.__init__ import application, people

blueprints = [
    [application, ''],
    [people, '/people']
]
