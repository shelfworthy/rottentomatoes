import re
import math
import requests

from .lists import List
from .movies import Movie

#  this is the current max the api will return per page
MAX_RESULTS = 50

class RottenTomatoesClient(object):
    def __init__(self, api_key):
        self.api_key = api_key

        self.server = 'api.rottentomatoes.com/api/public/v1.0/'

    def get_resource(self, url, params=None):
        if not re.match('http', url):
            url = "http://%s%s.json" % (self.server, url)

        request_params = {
            'apikey': self.api_key,
            'limit': MAX_RESULTS,
            'page_limit': MAX_RESULTS,
        }

        if params:
            request_params = dict(request_params.items() + params.items())

        response = requests.get(url, params=request_params, allow_redirects=True)
        response.raise_for_status()  # raise an error if we get one

        return response.json

    def parse_results(self, results):
        ''' takes results from search or lists and puts it in a nice format.
        '''

        if 'movies' in results:
            # if we have movies, return them

            if 'total' in results:
                #  find how many pages of results we'll have based on the total count and the amount per page
                pages = int(math.ceil(results['total']/float(MAX_RESULTS)))
            else:
                pages = 1

            return {
                'pages': pages,
                'movies': [Movie(movie_data, self) for movie_data in results['movies']]
            }
        else:
            # otherwise we probably have more lists
            final_dict = {}

            for key in results['links'].keys():
                final_dict[key] = List(results['links'][key], self)

        return final_dict

    def search(self, query, page=1):
        raw = self.get_resource('movies', params={
            'q': query,
            'page': page
        })

        return self.parse_results(raw)

    def lists(self, directory=None, page=1):
        base_list_url = 'lists'

        if directory:
            base_list_url = base_list_url + '/' + directory

        return self.parse_results(self.get_resource(base_list_url, params={'page': page}))
