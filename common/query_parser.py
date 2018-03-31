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
        for key, value in self.schema.items():
            if value is dict:
                denormalized[key] = self._parse_dict(params.get(key))
            elif value is list:
                denormalized[key] = params.getlist(key)
            elif value is int:
                denormalized[key] = int(params.get(key)) if params.get(key) else None
            else:
                denormalized[key] = params.get(key)

        return denormalized


    def _parse_dict(self, val):
        """ Parse given parameters to dict """

        try:
            return literal_eval(val)
        except ValueError:
            return val
