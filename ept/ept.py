
import aiohttp
import aiofiles
import asyncio

import json

from .info import Info
from .hierarchy import Key, Bounds

import concurrent.futures


class Endpoint(object):
    def __init__(self, root):
        self.root = root
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)

        if 'http' in root or 'https' in root:
            self.remote = True
        else:
            self.remote = False

    async def download(self, session, url):
        async with session.get(url) as response:
            return await response.text()

    async def fetch(self, part=None):

        url = self.root
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

    def __init__(self, url, bounds=None, depthEnd=None):

        self.root_url = url
        self.key = Key()
        self.overlaps_dict = {}
        self.depthEnd = depthEnd
        self.queryBounds = bounds
        self.endpoint = Endpoint(self.root_url)

    def get_info(self):
        loop = asyncio.get_event_loop()
        info = loop.run_until_complete(self._get_info(self.endpoint, self.root_url))
        return info

    info = property(get_info)

    async def _get_info(self, endpoint, url):
        d = await endpoint.fetch('/ept.json')
        return Info(d)


    def count(self):
        info = self.get_info()
        self.key.coords = info.bounds

        loop = asyncio.get_event_loop()
        o = loop.run_until_complete(self._overlaps())

        return (sum(self.overlaps_dict.values()))

    async def _overlaps(self):
        k = Key()
        k.coords = self.key.coords

        f = "/ept-hierarchy/" + k.id() + ".json"

        d = await self.endpoint.fetch(f)
        hier = json.loads(d)
        await self.overlaps(self.endpoint, self.overlaps_dict, hier, k)

    async def overlaps( self,
                        endpoint,
                        overlaps_dict,
                        hier,
                        key):

        if (self.queryBounds):
            if not key.overlaps(self.queryBounds):
                return


        if self.depthEnd:
            if key.d >= self.depthEnd:
                 return

        try:
            numPoints = hier[key.id()]
        except KeyError:
            hier[key.id()] = 0
            numPoints = 0
            return


        if numPoints == -1:
            # fetch more hierarchy

            f = "/ept-hierarchy/" + key.id() + ".json"
            data = await self.endpoint.fetch(f)
            hier = json.loads(data)
            await self.overlaps(self.endpoint,
                                self.overlaps_dict,
                                hier,
                                key)

        else:
            # check overlaps in each direction

            self.overlaps_dict[key] = numPoints
            bisected = key
            for direction in range(8):
                bisected = key.bisect(direction)
                await self.overlaps(self.endpoint,
                                    self.overlaps_dict,
                                    hier,
                                    bisected)
#

