""" Our own threadpool implementation.

- It is only slightly faster than the stdlib implementation.
- It behaves like a generator.
- It is used by the search indexer.

"""

import logging
import threading
import Queue as queue

log = logging.getLogger(__name__)


class Done(StopIteration):
    pass


class Worker(object):
    def __init__(self, in_queue, out_queue, func):
        self.in_queue = in_queue
        self.out_queue = out_queue
        self.func = func

    def run(self):
        in_queue = self.in_queue
        out_queue = self.out_queue
        func = self.func
        try:
            while True:
                item = in_queue.get(False)
                result = func(item)
                out_queue.put(result)
        except queue.Empty:
            pass
        finally:
            out_queue.put(Done)


class ThreadPool(object):
    def __init__(self, N):
        self.N = N

    def map(self, func, items):
        in_queue = queue.Queue()
        out_queue = queue.Queue()

        workers = [
            threading.Thread(target=Worker(in_queue, out_queue, func).run)
            for i in range(self.N)]
        workers_working = self.N

        for item in items:
            in_queue.put(item)

        log.info('Starting workers.')
        [worker.start() for worker in workers]
        log.info("workers started")

        while workers_working != 0:
            result = out_queue.get(True)

            if result is Done:
                workers_working -= 1
                continue

            yield result
