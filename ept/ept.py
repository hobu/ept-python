#
# EPT module
#
import os
import json
from urllib.parse import urlsplit, SplitResult

import aiohttp
import asyncio
import numpy

from .info import Info
from .hierarchy import Key
from .endpoint import Endpoint
from .pool import TaskPool
from .laz import LAZ


class EPT(object):
    def __init__(self, url, bounds=None, queryResolution=None):
        query = None
        if ('?' in url):
            [url, query] = url.split('?', 1)

        if url.endswith("/"):
            url = url[:-1]

        if url.endswith(".json"):
            # gave us path to EPT root
            p = urlsplit(url)
            url = SplitResult(p.scheme, p.netloc, os.path.dirname(p.path), "", "").geturl()

        self.query = query
        self.root_url = url
        self.key = Key()
        self.overlaps_dict = {}
        self.depthEnd = None
        self.queryResolution = queryResolution
        self.queryBounds = bounds
        self.endpoint = Endpoint(self.root_url, self.query)
        self.info = self.get_info()
        self.computedDepth = False

    def as_laspy(self, strictbounds=True):
        """
        Method to return a single LasData object for an ept query.
        """

        def filter(las, xmin, ymin, zmin, xmax, ymax, zmax):
            return las.points.array[
                (las.x >= xmin)
                & (las.x < xmax)
                & (las.y >= ymin)
                & (las.y < ymax)
                & (las.z >= zmin)
                & (las.z < zmax)
            ]

        las_objects = self.data()
        if las_objects:
            las = las_objects[0].las
            if strictbounds:
                las.points.array = numpy.concatenate(
                    [filter(l.las, *self.queryBounds.coords) for l in las_objects]
                )
            else:
                las.points.array = numpy.concatenate(
                    [l.las.points.array for l in las_objects]
                )
        else:
            las = None

        return las

    def get_info(self):
        d = self.endpoint.get("/ept.json")
        info = Info(d)
        return info

    def count(self):
        loop = asyncio.get_event_loop()
        o = loop.run_until_complete(self.overlaps())
        return sum(k.count for k in self.overlaps_dict)

    def data(self):
        loop = asyncio.get_event_loop()
        if not self.overlaps_dict:
            o = loop.run_until_complete(self.overlaps())
        o = loop.run_until_complete(self.adata())
        return o

    async def adata(self):
        limit = 10
        connector = aiohttp.TCPConnector(limit=None)
        async with aiohttp.ClientSession(connector=connector) as session, TaskPool(
            limit
        ) as tasks:

            for key in self.overlaps_dict:
                url = "/ept-data/" + key.id() + ".laz"
                await tasks.put(self.endpoint.aget(url, session))

        laz = [LAZ(tasks.data[i]["result"]) for i in tasks.data]
        return laz

    async def overlaps(self):
        k = Key()
        k.coords = self.info.bounds

        f = "/ept-hierarchy/" + k.id() + ".json"

        async with aiohttp.ClientSession() as session:
            d = await self.endpoint.aget(f, session)
            hier = json.loads(d)
            await self._overlaps(self.endpoint, self.overlaps_dict, hier, k, session)

    async def _overlaps(self, endpoint, overlaps_dict, hier, key, session):

        if self.queryBounds:
            if not key.overlaps(self.queryBounds):
                return

        # if we have already set self.depthEnd
        # dont set it again
        if self.queryResolution and not self.computedDepth and not self.depthEnd:
            currentResolution = (
                self.info.bounds[3] - self.info.bounds[0]
            ) / self.info.span

            self.depthEnd = 1
            while currentResolution > self.queryResolution:
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
            await self._overlaps(self.endpoint, self.overlaps_dict, hier, key, session)

        else:
            # check overlaps in each direction
            key.count = numPoints
            self.overlaps_dict[key] = key
            for direction in range(8):
                await self._overlaps(
                    self.endpoint,
                    self.overlaps_dict,
                    hier,
                    key.bisect(direction),
                    session,
                )
