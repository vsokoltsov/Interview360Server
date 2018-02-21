from ast import literal_eval
import ipdb

class QueryParser:
    """ Base class for parsing the query """

    def __init__(self, schema):
        """ Initialize class; Set schema value """

        self.schema = schema

    def parse(self, params):
        """ Parse given parameters in order to match the schema """

        denormalized = {}
        for key, value in params.items():
            key_type = self.schema.get(key)
            if key_type is dict:
                denormalized[key] = self._parse_dict(value)
            else:
                denormalized[key] = value

        return denormalized


    def _parse_dict(self, val):
        """ Parse given parameters to dict """

        try:
            return literal_eval(value)
        except ValueError:
            return value

    def _parse_arr(self, val):
        """ Parse given parameters to arr """
        pass
