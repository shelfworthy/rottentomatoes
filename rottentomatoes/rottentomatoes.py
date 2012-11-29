import re
import math

import requests

class rt(object):
    def __init__(self, api_key):
        self.api_key = api_key

        self.server = 'api.rottentomatoes.com/api/public/v1.0/'

        self.lists_url = self.server + '/lists'
        self.movie_url = self.server + '/movies'

    def _request(self, url, params=None):
        if not re.match('http', url):
            url = "http://%s%s.json" % (self.server, url)

        print url

        request_params = {'apikey': self.api_key}

        if params:
            request_params = dict(request_params.items() + params.items())

        response = requests.get(url, params=request_params, allow_redirects=True)
        response.raise_for_status()  # raise an error if we get one

        return response.json

    def search(self, query, page=1):
        """
        Rotten Tomatoes movie search. Returns a dict with two keys, pages and a dict of movies.

        >>> api = rt('my-api-key')
        >>> api.search('brave')


        {
            'pages': 2,
            'movies': {<movies here>}
        }

        """

        max_results_per_page = 50  # as set by the API

        raw = self._request('movies', params={
            'q': query,
            'page_limit': max_results_per_page,
            'page': page
        })

        total = raw['total']

        if total > max_results_per_page:
            count = total/float(max_results_per_page)
            number_of_pages = math.ceil(count)

        return {
            'pages': int(number_of_pages),
            'movies': raw['movies']
        }

    def lists(self, directory=None, sub=None, **kwargs):
        """
        Displays the lists available in the Rotten Tomatoes API.

        >>> rt().lists()
        {u'links': {u'movies': u'http://link-to-movies'
                    u'dvds': u'http://link-to-dvds'}
        >>> rt().lists('dvds')
        {u'links': {u'new_releases': u'http://link-to-new-releases'}
        >>> rt().lists('dvds', 'new_releases')
        """
        lists_url = [self.lists_url]
        if directory:
            if sub:
                lists_url.append('/%s/%s' % (directory, sub))
            else:
                lists_url.append('/%s' % directory)
        kwargs.update({'apikey': self.api_key})
        lists_url.extend(['.json?', urlencode(kwargs)])
        data = json.loads(urlopen(''.join(lists_url)).read())
        return data

    def info(self, id_num, specific_info=None):
        """
        Return info for a movie given its `id`.
        Arguments for `specific_info` include `cast` and `reviews`.

        >>> fight_club = u'13153'
        >>> rt().info(fight_club)
        >>> # For cast info
        ... rt().info(fight_club, 'cast')
        """
        if isinstance(id_num, int):
            id_num = str(id_num)
        movie_url = [self.movie_url]
        movie_url.append('/%s' % id_num)
        if specific_info:
            movie_url.append('/%s' % specific_info)
        end_of_url = ['.json?', urlencode({'apikey': self.api_key})]
        movie_url.extend(end_of_url)
        data = json.loads(urlopen(''.join(movie_url)).read())
        return data

    def new(self, kind='movies', **kwargs):
        """
        Short method to return just opened theatrical movies or newly
        released dvds. Returns a list of dictionaries.

        >>> rt().new('dvds', page_limit=5)
        """
        if kind == 'movies':
            return self.lists('movies', 'opening', **kwargs)['movies']
        elif kind == 'dvds':
            return self.lists('dvds', 'new_releases', **kwargs)['movies']

    def movies(self, sub='in_theaters', **kwargs):
        """
        Short method for returning specific movie lists.
        Possible sub aruments include: `box_office`, `in_theaters`,
        `opening`, and `upcoming`.

        >>> rt().movies('in_theaters', page_limit=5)
        """
        return self.lists('movies', sub, **kwargs)['movies']

    def dvds(self, sub='new_releases', **kwargs):
        """
        Short method for returning specific movie lists.
        Currently, only one sub argument is possible: `new_releases`.

        >>> rt().dvds(page_limit=5)
        """
        return self.lists('dvds', sub, **kwargs)['movies']

    def feeling_lucky(self, search_term):
        """
        Similar to Google's **I'm Feeling Lucky** button.
        Returns first instance of search term.

        >>> rt().feeling_lucky('memento')
        """
        return self.search(search_term, page_limit=1)[0]
