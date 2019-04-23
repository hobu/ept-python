
import aiohttp
import aiofiles
import asyncio

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

    async def download(self, session, url):
        async with session.get(url) as response:
            return await response.text()

    async def fetch(self, part=None):

        url = self.url
        if part:
            url = url + part

        if self.remote:
            async with aiohttp.ClientSession() as session:
                j = await self.download(session, url)
                return j
        else:
            async with aiofiles.open(url, 'rb') as d:
                data = await d.read()
                return data

class EPT(object):

    def __init__(self, url, bounds=None):

        self.root_url = url
        self.key = Key()
        self.overlaps_dict = {}
        self.depthEnd = float('inf')
        self.queryBounds = bounds
        self.endpoint = Endpoint(self.root_url)

    def get_info(self):
        loop = asyncio.get_event_loop()
        info = loop.run_until_complete(self._get_info(self.endpoint, self.root_url))
        self.key.coords = info.bounds
        return info

    info = property(get_info)

    async def _get_info(self, endpoint, url):
        d = await endpoint.fetch('/ept.json')
        return Info(d)


    def count(self):
        loop = asyncio.get_event_loop()
        o = loop.run_until_complete(self._overlaps())
        return o

    async def _overlaps(self):
        k = Key()
        k.coords = self.key.coords

        f = "/ept-hierarchy/" + k.id() + ".json"

        d = await self.endpoint.fetch(f)
        hier = json.loads(d)


        await self.overlaps(self.endpoint, self.overlaps_dict, hier, k)

    async def overlaps(   self,
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
        data = await self.endpoint.fetch(f)
        hier = json.loads(data)


        await overlaps(self.endpoint, self.overlaps_dict, hier, k)


        print ("checking overlaps")

