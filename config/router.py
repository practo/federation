from federation_api.application.api.__init__ import application
from federation_api.people.api.__init__ import people

blueprints = [
    [application, ''],
    [people, '/people']
]
