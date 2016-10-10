from flask import Blueprint

people = Blueprint('people', __name__)

battalion = 'people'

module = {
    'api': [
        'people',
    ]
}

for squadron, squadron_classes in module.iteritems():
    for squadron_class in squadron_classes:
        __import__('federation_api.{0}.{1}.{2}'.format(battalion,
                                                       squadron,
                                                       squadron_class))
