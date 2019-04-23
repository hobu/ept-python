

import requests
import json

from .info import Info
from .hierarchy import Key

import concurrent.futures


class Endpoint(object):
    def __init__(self, url):
        self.url = url
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)

        if 'http' in url or 'https' in url:
            self.remote = True
        else:
            self.remote = False

    def fetch(self, part=None):
        url = self.url
        if part:
            url = url + part

        if self.remote:
            data = requests.get(self.url).json()
        else:
            with open(url, 'rb') as d:
                data = d.read()
        return data

class EPT(object):

    def __init__(self, url, bounds=None):

        self.key = Key()
        endpoint = Endpoint(url)
        self.info = self._get_info(endpoint, url)
        self.key.coords = self.info.bounds
        self.overlaps_dict = {}
        self.endpoint = endpoint
        self.depthEnd = float('inf')
        self.queryBounds = bounds




    def _get_info(self, endpoint, url):
        part = None
        if '.json' not in url:
            part = '/ept.json'

        return Info(endpoint.fetch(part))


    def count(self):
        self._overlaps()

    def _overlaps(self):
        k = Key()
        k.coords = self.key.coords

        f = "/ept-hierarchy/" + k.id() + ".json"
        hier = json.loads(self.endpoint.fetch(f))


        self.overlaps(self.endpoint, self.overlaps_dict, hier, k)

    def overlaps(   self,
                    endpoint,
                    overlaps_dict,
                    hier,
                    key):
        if not key.overlaps(self.queryBounds):
            return

        if self.depthEnd and key.d >= self.depthEnd:
            return

        k.coords = self.key.coords

        f = "/ept-hierarchy/" + k.id() + ".json"
        hier = json.loads(self.endpoint.fetch(f))


        overlaps(self.endpoint, self.overlaps_dict, hier, k)


        print ("checking overlaps")

