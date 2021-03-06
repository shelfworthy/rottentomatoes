class List(object):
    def __init__(self, url, client):
        self.url = url
        self.client = client

    def get(self):
        return self.client.parse_results(self.client.get_resource(self.url))
