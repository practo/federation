import json
from copy import deepcopy
from inflection import underscore, pluralize


class StarFleetHelper():
    @classmethod
    def serialize_as_json(self, star_fleet_instance, *droid_names, **config):
        star_fleet_json = {}
        for droid_name in droid_names:
            if(hasattr(star_fleet_instance, droid_name)):
                droid_value = getattr(star_fleet_instance, droid_name)
                star_fleet_json[droid_name] = json.dumps(droid_value) \
                    if type(droid_value) is dict else droid_value
        star_fleet_instance_json = {}
        if(config.get('root', True)):
            star_fleet_json_root = config.get('root_name',
                                              underscore(type(
                                                         star_fleet_instance
                                                         ).__name__))
            star_fleet_instance_json[star_fleet_json_root] = star_fleet_json
        else:
            star_fleet_instance_json = star_fleet_json
        return star_fleet_instance_json

    @classmethod
    def bulk_serialize_as_json(self, star_fleet_instances,
                               *droid_names, **config):
        if(type(star_fleet_instances) is not list or not star_fleet_instances):
            raise TypeError
        star_fleets_json = {}
        instance_config = deepcopy(config)
        instance_config['root'] = False
        star_fleets = []
        for star_fleet_instance in star_fleet_instances:
            star_fleets.append(self.serialize_as_json(star_fleet_instance,
                                                      *droid_names,
                                                      **instance_config))
        if(config.get('root', True)):
            star_fleets_json_root = config.get(
                'root_name',
                pluralize(underscore(type(star_fleet_instances[0]).__name__)))
            star_fleets_json[star_fleets_json_root] = star_fleets
        else:
            star_fleets_json = star_fleets
        return star_fleets_json
