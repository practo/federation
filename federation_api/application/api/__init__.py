from flask import Blueprint
from star_fleet_api import StarFleetAPI, \
    NotFoundException, RequestParametersException, UnprocessibleEntryException

application = Blueprint('application', __name__)

battalion = 'application'

module = {
    'api': [
        'application',
    ]
}

for squadron, squadron_classes in module.iteritems():
    for squadron_class in squadron_classes:
        __import__('federation_api.{0}.{1}.{2}'.format(battalion,
                                                       squadron,
                                                       squadron_class))
