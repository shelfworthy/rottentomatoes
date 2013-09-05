from datetime import datetime

class Movie(object):
    def __init__(self, raw_json, client):
        self.client = client

        self.data = raw_json

    def __getattr__(self, name):
        return self.get_info(name)

    @property
    def url(self):
        return self.data['links']['self']

    @property
    def year(self):
        return int(self.data['year'])

    @property
    def imdb_id(self):
        if 'imdb' in self.data['alternate_ids']:
            return self.data['alternate_ids']['imdb']

    @property
    def critics_score(self):
        return int(self.data['ratings']['critics_score'])

    @property
    def theater_date(self):
        if 'theater' in self.data['release_dates']:
            return datetime.strptime(self.data['release_dates']['theater'], '%Y-%m-%d').date()

    @property
    def dvd_date(self):
        return datetime.strptime(self.data['release_dates']['dvd'], '%Y-%m-%d').date()

    def get_info(self, key):
        '''
        This function will get the given key from the resource.
        If the data has already been downloaded, its returned.
        If the data hasn't been downloaded, this function hits
        the server to fill out more data about this item.

        key: the key to get info from

        '''

        if not key in self.data:
            # see if what the user is looking for is still on the server
            if 'links' in self.data and key in self.data['links']:
                resource = self.client.get_resource(self.data['links'][key])
                self.data[key] = resource[key]

        if key in self.data:
            return self.data[key]

        return None
