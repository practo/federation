import json
import datetime
from copy import deepcopy
from inflection import underscore, pluralize


def set_root_name(object, root_name=None):
    if(root_name):
        return root_name
    else:
        if(object):
            object_type = type(object)
            if(object_type is list):
                return pluralize(
                    underscore(type(object[0]).__name__))
            else:
                return underscore(object_type.__name__)
        else:
            raise KeyError("Cannot automatically determine type, "
                           "please provide 'root_name' explicitly.")


def format_droid_value(droid_value, datetime_format=None):
    droid_value_type = type(droid_value)
    if(droid_value_type is dict):
        return json.dumps(droid_value)
    elif(droid_value_type is datetime.datetime):
        if(datetime_format):
            return droid_value.strftime(datetime_format)
        else:
            return droid_value
    else:
        return droid_value


def make_json(root, object, root_name, value):
    if(root):
        root_name = set_root_name(object, root_name)
        object_type = type(object)
        if(object_type is list):
            return {root_name: value, 'total': len(value)}
        else:
            return {root_name: value}
    else:
        return value


class StarFleetsHelper():
    @classmethod
    def serialize_as_json(self, star_fleet_instance, *droid_names, **config):
        datetime_format = config.get('datetime_format', '%s')
        star_fleet_json = {}
        for droid_name in droid_names:
            if(droid_name):
                if(hasattr(star_fleet_instance, droid_name)):
                    droid_value = getattr(star_fleet_instance, droid_name)
                    star_fleet_json[droid_name] = format_droid_value(
                        droid_value, datetime_format)
        star_fleet_instance_json = make_json(
            config.get('root', True), star_fleet_instance,
            config.get('root_name'), star_fleet_json)

        return star_fleet_instance_json

    @classmethod
    def bulk_serialize_as_json(self, star_fleet_instances,
                               *droid_names, **config):
        star_fleet_instances = star_fleet_instances or []
        star_fleets_json = {}
        instance_config = deepcopy(config)
        instance_config['root'] = False
        star_fleets = []
        for star_fleet_instance in star_fleet_instances:
            star_fleets.append(self.serialize_as_json(star_fleet_instance,
                                                      *droid_names,
                                                      **instance_config))
        star_fleets_json = make_json(
            config.get('root', True), star_fleet_instances,
            config.get('root_name'), star_fleets)

        return star_fleets_json
