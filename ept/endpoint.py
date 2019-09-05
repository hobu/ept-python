import aiohttp
import aiofiles
import asyncio

import json
from .pool import TaskPool


class Driver(object):
    def __init__(self, root, concurrency=1):
        self.root = root
        self.parts = []
        self.concurrency = concurrency

class Http(Driver):
    def __init__(self, root):
        super(Http, self).__init__(root)

    async def download(self, session, url):
        async with session.get(url) as response:
            return await response.read()

    async def get(self, part, session = None, tpool=None):
        url = self.root + part
        if tpool:
            return await tpool.put(self.download(session, url))
        if session:
            async with session.get(url) as response:
                return await response.read()
        else:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    return await response.read()

    def stage(self, part):
        self.parts.append(part)

    async def bulk(self):
        connector = aiohttp.TCPConnector(limit=None)
        async with aiohttp.ClientSession(connector=connector) as session, TaskPool(self.concurrency) as tasks:
            for part in self.parts:
                await tasks.put(self.download(session, self.root + part))

        return tasks
#         print ('task returns:', len(tasks.data))
#         k = list(tasks.data.keys())[0]
#         t = tasks.data[k]
#         return t['result']
#
#         raise (t['exception'])

class File(Driver):
    def __init__(self, root):
        super(File, self).__init__(root)

    async def get(self, part, session=None, tpool=None):
        url = self.root
        if part:
            url = url + part

        async with aiofiles.open(url, 'rb') as d:
            return await d.read()



class Endpoint(object):
    def __init__(self, root):
        self.root = root

        if 'http' in root or 'https' in root:
            self.remote = True
            self.driver = Http(root)
        else:
            self.remote = False
            self.driver = File(root)

    def get(self, part):
        loop = asyncio.get_event_loop()
        o = loop.run_until_complete(self.driver.get(part))
        return o

    async def aget(self, part=None, session=None, tpool=None):
        return await self.driver.get(part, session, tpool)

