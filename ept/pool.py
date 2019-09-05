import aiohttp
import asyncio


# Adapted from https://medium.com/@cgarciae/making-an-infinite-number-of-requests-with-python-aiohttp-pypeln-3a552b97dc95
class TaskPool(object):
    """TaskPool for doing lots of stuff with a semaphore"""

    def __init__(self, workers):
        self._semaphore = asyncio.Semaphore(workers)
        self._tasks = set()
        self.data = {}

    async def put(self, coro):
        await self._semaphore.acquire()

        # cache our coro's args
        args = coro.cr_frame.f_locals
        self.data[id(coro)] = {'args': args }

        # add the task
        task = asyncio.ensure_future(coro)
        self._tasks.add(task)
        task.add_done_callback(self._on_task_done)

    def _on_task_done(self, task):
        k = id(task._coro)
        try:
            self.data[k]['result'] = task.result()
        except:
            self.data[k]['result'] = None
        self.data[k]['exception'] = task.exception()
        self._tasks.remove(task)
        self._semaphore.release()

    async def join(self):
        await asyncio.gather(*self._tasks, return_exceptions=True)

    async def __aenter__(self):
        return self

    def __aexit__(self, exc_type, exc, tb):
        return self.join()
