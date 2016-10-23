from inflection import underscore
from config.initializers.errors import NotFoundException, \
    ParametersException, UnprocessibleEntryException


class StarFleets():
    @classmethod
    def set_instance(self, model, id):
        instance = model.find(id)
        if(not instance):
            raise NotFoundException(model=model.__name__, attribute='id',
                                    value=id)

        return instance

    @classmethod
    def droid_parameters(self, parameters, droid_key):
        if(parameters is None or droid_key not in parameters.keys()):
            raise ParametersException('is missing', droid_key)

        return parameters[droid_key]

    @classmethod
    def sanitized_parameters(self, model, parameters, *droid_names):
        droid_key = underscore(model.__name__)
        model_parameters = self.droid_parameters(parameters, droid_key)
        sanitized_droid_names = {}
        missing_droid_names = []
        for droid_name in droid_names:
            try:
                sanitized_droid_names[droid_name] = \
                    model_parameters[droid_name]
            except KeyError:
                missing_droid_names.append('.'.join([droid_key, droid_name]))
        if(missing_droid_names):
            raise ParametersException('is missing', *missing_droid_names)

        return sanitized_droid_names

    @classmethod
    def permitted_parameters(self, model, parameters, *droid_names):
        droid_key = underscore(model.__name__)
        model_parameters = self.droid_parameters(parameters, droid_key)
        permitted_droid_names = {}
        unpermitted_droid_names = []
        for droid_name in droid_names:
            parameter = model_parameters.get(droid_name, False)
            if(parameter):
                permitted_droid_names[droid_name] = parameter
        unpermitted_droid_names = ['.'.join([droid_key, key])
                                   for key in model_parameters.keys()
                                   if key not in droid_names]
        if(unpermitted_droid_names):
            raise ParametersException('cannot be updated',
                                      *unpermitted_droid_names)

        return permitted_droid_names

    @classmethod
    def process_instance(self, droid):
        if(droid.errors):
            raise UnprocessibleEntryException(droid.errors)
