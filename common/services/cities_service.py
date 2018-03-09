import requests
import os
import json

class CitiesService:
    """ Service for getting the cities list from geonames.com """

    DEFAULT_ENCODING = 'utf-8'
    URL = 'http://api.geonames.org/search'
    FORMAT_TYPE = 'json'

    def __init__(self):
        """ Initialize method for cities service """

        self.objects = []
        self.errors = None

    def find_exact_name(self, name):
        """ Receive a list of matched cities by the name """

        username = os.environ('GEONAMES_USER')
        params = {
            'name_equals': name,
            'type': self.FORMAT_TYPE,
            'username': username
        }
        request = requests.get(self.URL, params=params)
        json_result = json.loads(result.decode(self.DEFAULT_ENCODING))
        if json_result.get('status'):
            self.errors = json_result.get('status')
            return False
        else:
            self.objects = json_result
            return True
