
import aiohttp
import aiofiles
import asyncio

import json

from .info import Info
from .hierarchy import Key, Bounds
from .endpoint import Endpoint

import concurrent.futures

class EPT(object):

    def __init__(self,  url,
                        bounds = None,
                        queryResolution = None):

        self.root_url = url
        self.key = Key()
        self.overlaps_dict = {}
        self.depthEnd = None
        self.queryResolution = queryResolution
        self.queryBounds = bounds
        self.endpoint = Endpoint(self.root_url)
        self.info = self.get_info()
        self.computedDepth = False


    def get_info(self):
        d = self.endpoint.get('/ept.json')
        info = Info(d)
        return info

    def count(self):
        loop = asyncio.get_event_loop()
        o = loop.run_until_complete(self.overlaps())
        return (sum(self.overlaps_dict.values()))

    async def overlaps(self):
        k = Key()
        k.coords = self.info.bounds

        f = "/ept-hierarchy/" + k.id() + ".json"

        async with aiohttp.ClientSession() as session:
            d = await self.endpoint.aget(f, session)
            hier = json.loads(d)
            await self._overlaps(self.endpoint, self.overlaps_dict, hier, k, session)

    async def _overlaps( self,
                        endpoint,
                        overlaps_dict,
                        hier,
                        key,
                        session):

        if self.queryBounds:
            if not key.overlaps(self.queryBounds):
                return

        # if we have already set self.depthEnd
        # dont set it again
        if self.queryResolution and not self.computedDepth and not self.depthEnd:
            currentResolution = (self.info.bounds[3] - self.info.bounds[0]) / self.info.span

            self.depthEnd = 1
            while (currentResolution > self.queryResolution):
                currentResolution = currentResolution / 2.0
                self.depthEnd = self.depthEnd + 1
            self.computedDepth = True

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
            data = await self.endpoint.aget(f, session)
            hier = json.loads(data)
            await self._overlaps(self.endpoint,
                                self.overlaps_dict,
                                hier,
                                key,
                                session)

        else:
            # check overlaps in each direction
            self.overlaps_dict[key] = numPoints
            for direction in range(8):
                await self._overlaps(self.endpoint,
                                    self.overlaps_dict,
                                    hier,
                                    key.bisect(direction), session)

