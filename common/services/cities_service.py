import requests
import os
import json
import ipdb

class CitiesService:
    """ Service for getting the cities list from geonames.com """

    URL = 'https://maps.googleapis.com/maps/api/place/autocomplete/{}'
    FORMAT_TYPE = 'json'
    REQUEST_DENIED = 'REQUEST_DENIED'

    def __init__(self):
        """ Initialize method for cities service """

        self.objects = []
        self.errors = None
        self.api_key = os.environ.get('GOOGLE_PLACES_API')

    def find_by_name(self, name):
        """ Receive a list of matched cities by the name """

        params = {
            'input': name,
            'types': '(cities)',
            'key': self.api_key
        }
        request = requests.get(
            self.URL.format(self.FORMAT_TYPE), params=params
        )
        result = request.json()
        if result.get('status') == self.REQUEST_DENIED:
            return []
        json_result = result.get('predictions')
        return [
            {
              'city': item.get('structured_formatting').get('main_text'),
              'country': item.get('structured_formatting').get('secondary_text')
             } for item in json_result
        ]
