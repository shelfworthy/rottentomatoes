import re
import math

import requests

#  this is the current max the api will return per page
max_results_per_page = 50

def parse_list(results, api_key):
    if 'movies' in results:
        # if we have movies, return them

        if 'total' in results:
            #  find how many pages of results we'll have based on the total count and the amount per page
            pages = int(math.ceil(results['total']/float(max_results_per_page)))
        else:
            pages = 1

        return {
            'pages': pages,
            'movies': results['movies']
        }

        return results['movies']
    else:
        # otherwise we probably have more lists
        final_dict = {}

        for key in results['links'].keys():
            final_dict[key] = List(results['links'][key], api_key)

        return final_dict

class List(object):
    def __init__(self, url, api_key):
        self.url = url
        self.api_key = api_key

    def get(self):
        results = RottenTomatoesClient(self.api_key)._request(self.url)

        return parse_list(results, self.api_key)

class RottenTomatoesClient(object):
    def __init__(self, api_key):
        self.api_key = api_key

        self.server = 'api.rottentomatoes.com/api/public/v1.0/'

    def _request(self, url, params=None):
        if not re.match('http', url):
            url = "http://%s%s.json" % (self.server, url)

        request_params = {
            'apikey': self.api_key,
            'limit': max_results_per_page,
            'page_limit': max_results_per_page,
        }

        if params:
            request_params = dict(request_params.items() + params.items())

        response = requests.get(url, params=request_params, allow_redirects=True)
        response.raise_for_status()  # raise an error if we get one

        return response.json

    def search(self, query, page=1):
        """
        Rotten Tomatoes movie search. Returns a dict with two keys, pages and a dict of movies.

        >>> api = RottenTomatoesClient('my-api-key')
        >>> api.search('brave')


        {
            'pages': 2,
            'movies': {<movies here>}
        }

        """

        raw = self._request('movies', params={
            'q': query,
            'page': page
        })

        return parse_list(raw, self.api_key)

    def lists(self, directory=None, page=1):
        """
        If sent without a directory returns the lists available in the Rotten Tomatoes API.

        >>> api = RottenTomatoesClient('my-api-key')
        >>> lists = api.lists()

        {u'dvds': <rottentomatoes.rottentomatoes.List at 0x1032d0690>,
         u'movies': <rottentomatoes.rottentomatoes.List at 0x1032d06d0>}

        >>> dvd_lists = lists['dvd'].get()

        {u'current_releases': <rottentomatoes.rottentomatoes.List at 0x1032db050>,
         u'new_releases': <rottentomatoes.rottentomatoes.List at 0x1032db350>,
         u'top_rentals': <rottentomatoes.rottentomatoes.List at 0x1032db250>,
         u'upcoming': <rottentomatoes.rottentomatoes.List at 0x1032db0d0>}

        >>> dvd_lists['current_releases'].get()

        {
            'pages': 2,
            'movies': {<movies here>}
        }
        """

        base_list_url = 'lists'

        if directory:
            base_list_url = base_list_url + '/' + directory

        return parse_list(self._request(base_list_url), self.api_key)
