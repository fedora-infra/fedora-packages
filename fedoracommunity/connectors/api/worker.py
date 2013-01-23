#!/usr/bin/env python
""" This is a long-running worker process that generates values asychronously
for dogpile.cache and the fcomm_connector api.

It should be run under a sysvinit script as a daemon.  It should be run as 8 or
so threads.
"""

import tg
import os
import sys
import json
import time
import types
import retask.queue
import memcache
import threading

from paste.deploy import appconfig

import dogpile.cache.api
import dogpile.cache.region

# Initialize an incoming redis queue right off the bat.
queue = retask.queue.Queue('fedora-packages')
queue.connect()

config = appconfig('config:development.ini', relative_to=os.getcwd())
tg.config = config

# Disable all caching so we don't cyclically cache ourselves into a corner
for key in list(tg.config.keys()):
    if 'cache.connector' in key:
        del tg.config[key]

from fedoracommunity.connectors.api.mw import FCommConnectorMiddleware
mw_obj = FCommConnectorMiddleware(lambda *args, **kw: None)

threads = []


class fake_request(object):
    environ = {}


class Thread(threading.Thread):
    def iteration(self):
        if queue.length == 0:
            print("No tasks found in the queue.  Sleeping for 2 seconds.")
            return

        task = queue.dequeue()
        data = json.loads(task.data)

        mc = memcache.Client(data['memcached_addrs'])

        try:
            # Here are those three attribute that we hung
            # on the original cached fn
            name = data['fn']['name']
            path = data['fn']['path']
            typ = data['fn']['type']

            conn_cls = mw_obj._connectors[name]['connector_class']

            request = fake_request()
            conn_obj = conn_cls(request.environ, request)

            if typ == 'query':
                fn = conn_obj._query_paths[path]['query_func']
            else:
                fn = conn_obj._method_paths[path]

            fn = types.MethodType(fn, conn_obj, conn_cls)

            print "Calling {name}(**{kw})".format(
                name=repr(fn), kw=data['kw'])

            value = fn(**data['kw'])

            value = dogpile.cache.api.CachedValue(value, {
                "ct": time.time(),
                "v": dogpile.cache.region.value_version,
            })
            cache_key = str(data['cache_key'])
            print "Value Recorded at", cache_key
            mc.set(cache_key, value)
        finally:
            # Release the kraken!
            print "Mutex released."
            mc.delete(str(data['mutex_key']))

    def kill(self):
        self.die = True

    def run(self):
        self.die = False
        while not self.die:
            try:
                self.iteration()
            except KeyboardInterrupt:
                break
            except Exception:
                import traceback
                traceback.print_exc()
            time.sleep(2)
            sys.stdout.flush()


def main():
    def _handle_signal(self, signum, stackframe):
        for thread in threads:
            thread.kill()

    from daemon import DaemonContext
    try:
        from daemon.pidfile import TimeoutPIDLockFile as PIDLockFile
    except:
        from daemon.pidlockfile import PIDLockFile

    #pidlock = PIDLockFile('/var/run/fedoracommunity/worker.pid')
    #output = file('/var/log/fedoracommunity/worker.log', 'a')
    pidlock = PIDLockFile('/tmp/fedoracommunity-worker.pid')
    output = file('/tmp/fedoracommunity-worker.log', 'a')

    daemon = DaemonContext(pidfile=pidlock, stdout=output, stderr=output)
    daemon.terminate = _handle_signal

    n = 1
    with daemon:
        print "changing dir (just for development)"
        os.chdir("/home/threebean/devel/fedora-packages/")

        print "Creating %i threads" % n
        threads = [Thread() for i in range(n)]

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

if __name__ == '__main__':
    main()
