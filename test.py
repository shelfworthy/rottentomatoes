#!/usr/bin/env python

"""Unit tests for the `rottentomatoes.py` file."""

import unittest
try:
    from urlparse import urlparse, parse_qs
except ImportError:  # pragma: no cover
    # For older versions of Python.
    from urlparse import urlparse
    from cgi import parse_qs
from mock import Mock
from rottentomatoes import rottentomatoes
from rottentomatoes import rt


def set_up():
    """
    Mock both and json.loads' return value. Makes for fast unit tests.
    """
    rottentomatoes.urlopen = Mock()
    movies_dict = {'movies': ['first_result', 'second_result'],
                   'total': 2}
    rottentomatoes.json.loads = Mock(return_value=movies_dict)
    rottentomatoes.API_KEY = 'my_api_key'


def call_args(kind='query'):
    """Find out what urlopen called while mocking."""
    call = rottentomatoes.urlopen.call_args[0][0]
    parsed_call = urlparse(call)
    if kind == 'query':
        return  parse_qs(parsed_call.query)
    elif kind == 'path':
        return parsed_call.path


class rtClassInitTest(unittest.TestCase):

    def setUp(self):
        set_up()

    def test_uninitialized_api_key(self):
        self.assertEqual(rt().api_key, 'my_api_key')

    def test_initialized_api_key(self):
        self.assertEqual(rt('called_api_key').api_key, 'called_api_key')

    def test_version_argument_with_float(self):
        self.assertEqual(rt(version=2.5).version, '2.5')

    def test_version_argument_with_string(self):
        self.assertEqual(rt(version='2.5').version, '2.5')


class SearchMethodTest(unittest.TestCase):

    def setUp(self):
        set_up()

    def test_nonempty_search_url_path(self):
        rt().search('some movie')
        path = call_args('path')
        self.assertEqual(path, '/api/public/v1.0/movies')

    def test_empty_search_url_keys(self):
        rt().search('')
        movie = call_args()
        self.assertEqual(movie.keys(), ['apikey'])

    def test_nonempty_search_url_keys(self):
        rt().search('some movie')
        movie = call_args()
        self.assertEqual(movie.keys(), ['q', 'apikey'])

    def test_search_url_keys_with_page_arg(self):
        rt().search('some movie', page=2)
        movie = call_args()
        self.assertEqual(movie.keys(), ['q', 'apikey', 'page'])

    def test_search_url_keys_with_page_limit_arg(self):
        rt().search('some movie', page_limit=5)
        movie = call_args()
        self.assertEqual(movie.keys(), ['q', 'apikey', 'page_limit'])

    def test_search_url_keys_with_multiple_kwargs(self):
        rt().search('some movie', page=2, page_limit=5)
        movie = call_args()
        self.assertEqual(movie.keys(), ['q', 'apikey', 'page', 'page_limit'])

    def test_search_url_keys_for_lion_king(self):
        rt().search('the lion king')
        movie = call_args()
        assert 'my_api_key' in movie['apikey']
        assert 'the lion king' in movie['q']

    def test_search_url_keys_for_ronin(self):
        rt().search('ronin')
        movie = call_args()
        assert 'my_api_key' in movie['apikey']
        assert 'ronin' in movie['q']

    def test_search_results_for_standard_datatype(self):
        results = rt().search('some movie')
        self.assertEqual(results, ['first_result', 'second_result'])

    def test_search_results_for_movies_datatype(self):
        results = rt().search('some movie', 'movies')
        self.assertEqual(results, ['first_result', 'second_result'])

    def test_search_results_for_total_datatype(self):
        results = rt().search('some movie', 'total')
        self.assertEqual(results, 2)


class ListsMethodTest(unittest.TestCase):

    def setUp(self):
        set_up()

    def test_empty_lists_url_path(self):
        rt().lists()
        path = call_args('path')
        self.assertEqual(path, '/api/public/v1.0/lists.json')

    def test_lists_url_path_for_dvds(self):
        rt().lists('dvds')
        path = call_args('path')
        self.assertEqual(path, '/api/public/v1.0/lists/dvds.json')

    def test_lists_url_path_for_dvds_sub_new_releases(self):
        rt().lists('dvds', 'new_releases')
        path = call_args('path')
        self.assertEqual(path, '/api/public/v1.0/lists/dvds/new_releases.json')

    def test_lists_url_path_for_movies(self):
        rt().lists('movies')
        path = call_args('path')
        self.assertEqual(path, '/api/public/v1.0/lists/movies.json')

    def test_lists_url_path_for_movies_sub_opening(self):
        rt().lists('movies', 'opening')
        path = call_args('path')
        self.assertEqual(path, '/api/public/v1.0/lists/movies/opening.json')

    def test_lists_url_keys_for_extra_kwargs(self):
        rt().lists('movies', 'in_theaters', page_limit=5)
        parsed_query = call_args()
        assert 'my_api_key' in parsed_query['apikey']
        assert '5' in parsed_query['page_limit']


class InfoMethodTest(unittest.TestCase):

    def setUp(self):
        set_up()

    def test_empty_info_method_call_fails(self):
        self.assertRaises(TypeError, rt().info)

    def test_id_num_as_string(self):
        fight_club = '13153'
        rt().info(fight_club)
        path = call_args('path')
        self.assertEqual(path, '/api/public/v1.0/movies/13153.json')

    def test_id_num_as_int(self):
        fight_club = 13153
        rt().info(fight_club)
        path = call_args('path')
        self.assertEqual(path, '/api/public/v1.0/movies/13153.json')

    def test_specific_info_for_cast(self):
        fight_club = '13153'
        rt().info(fight_club, 'cast')
        path = call_args('path')
        self.assertEqual(path, '/api/public/v1.0/movies/13153/cast.json')

    def test_specific_info_for_reviews(self):
        fight_club = '13153'
        rt().info(fight_club, 'reviews')
        path = call_args('path')
        self.assertEqual(path, '/api/public/v1.0/movies/13153/reviews.json')


class NewMethodTest(unittest.TestCase):

    def setUp(self):
        set_up()

    def test_new_url_path_for_dvds(self):
        rt().new('dvds')
        path = call_args('path')
        self.assertEqual(path, '/api/public/v1.0/lists/dvds/new_releases.json')

    def test_new_url_keys_for_dvds_with_kwargs(self):
        rt().new('dvds', page=2)
        parsed_query = call_args()
        assert '2' in parsed_query['page']

    def test_new_url_path_for_movies(self):
        rt().new('movies')
        path = call_args('path')
        self.assertEqual(path, '/api/public/v1.0/lists/movies/opening.json')

    def test_new_url_keys_for_movies_with_kwargs(self):
        rt().new('movies', page_limit=5)
        parsed_query = call_args()
        assert '5' in parsed_query['page_limit']


class MoviesMethodTest(unittest.TestCase):

    def setUp(self):
        set_up()

    def test_empty_movies_call_reverts_to_in_theaters(self):
        rt().movies()
        path = call_args('path')
        expected_path = '/api/public/v1.0/lists/movies/in_theaters.json'
        self.assertEqual(path, expected_path)

    def test_movies_in_theaters(self):
        rt().movies('in_theaters')
        path = call_args('path')
        expected_path = '/api/public/v1.0/lists/movies/in_theaters.json'
        self.assertEqual(path, expected_path)

    def test_movies_upcoming(self):
        rt().movies('upcoming')
        path = call_args('path')
        expected_path = '/api/public/v1.0/lists/movies/upcoming.json'
        self.assertEqual(path, expected_path)

    def test_movies_opening(self):
        rt().movies('opening')
        path = call_args('path')
        expected_path = '/api/public/v1.0/lists/movies/opening.json'
        self.assertEqual(path, expected_path)

    def test_movies_box_office(self):
        rt().movies('box_office')
        path = call_args('path')
        expected_path = '/api/public/v1.0/lists/movies/box_office.json'
        self.assertEqual(path, expected_path)


class DvdsMethodTest(unittest.TestCase):

    def setUp(self):
        set_up()

    def test_empty_dvds_call_reverts_to_new_releases(self):
        rt().dvds()
        path = call_args('path')
        expected_path = '/api/public/v1.0/lists/dvds/new_releases.json'
        self.assertEqual(path, expected_path)

    def test_dvds_new_releases(self):
        rt().dvds('new_releases')
        path = call_args('path')
        expected_path = '/api/public/v1.0/lists/dvds/new_releases.json'
        self.assertEqual(path, expected_path)


class FeelingLuckyMethodTest(unittest.TestCase):

    def setUp(self):
        set_up()

    def test_empty_feeling_lucky_method_fails(self):
        self.assertRaises(TypeError, rt().feeling_lucky)

    def test_first_json_loads_movies_result_is_returned(self):
        data = rt().feeling_lucky('some movie')
        self.assertEqual(data, 'first_result')


if __name__ == '__main__':
    unittest.main()
