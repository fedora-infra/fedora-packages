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

threads = []

import logging
log = logging.getLogger("fcomm-cache-worker")


class fake_request(object):
    environ = {}


class Thread(threading.Thread):
    def init(self):
        self.die = False

        # Initialize an incoming redis queue right off the bat.
        self.queue = retask.queue.Queue('fedora-packages')
        self.queue.connect()

        config = appconfig("config:" + find_config_file())
        tg.config.update(config)

        # Disable all caching so we don't cyclically cache ourselves
        # into a corner
        for key in list(tg.config.keys()):
            if 'cache.connector' in key:
                del tg.config[key]

        from fedoracommunity.connectors.api.mw import FCommConnectorMiddleware
        self.mw_obj = FCommConnectorMiddleware(lambda *args, **kw: None)

    def iteration(self):
        if self.queue.length == 0:
            log.info("No tasks found in the queue.  Sleeping for 2 seconds.")
            return

        log.info("Picking up a task from the queue.")
        task = self.queue.dequeue()
        data = json.loads(task.data)

        mc = memcache.Client(data['memcached_addrs'])

        try:
            # Here are those three attribute that we hung
            # on the original cached fn
            name = data['fn']['name']
            path = data['fn']['path']
            typ = data['fn']['type']

            conn_cls = self.mw_obj._connectors[name]['connector_class']

            request = fake_request()
            conn_obj = conn_cls(request.environ, request)

            if typ == 'query':
                fn = conn_obj._query_paths[path]['query_func']
            else:
                fn = conn_obj._method_paths[path]

            fn = types.MethodType(fn, conn_obj, conn_cls)

            log.info("Calling {name}(**{kw})".format(
                name=repr(fn), kw=data['kw']))

            value = fn(**data['kw'])

            value = dogpile.cache.api.CachedValue(value, {
                "ct": time.time(),
                "v": dogpile.cache.region.value_version,
            })
            cache_key = str(data['cache_key'])
            log.debug("Value Recorded at " + cache_key)
            mc.set(cache_key, value)
        finally:
            # Release the kraken!
            log.info("Mutex released.")
            mc.delete(str(data['mutex_key']))

    def run(self):
        self.init()
        while not self.die:
            try:
                self.iteration()
            except KeyboardInterrupt:
                break
            except Exception:
                import traceback
                log.error(traceback.format_exc())
            time.sleep(2)
            sys.stdout.flush()
        log.info("Thread exiting.")


    def kill(self):
        self.die = True

def find_config_file():
    locations = (
        '.',
        '/etc/fedoracommunity/',
        '/'.join(__file__.split('/') + ['..', '..', '..', '..']),
    )
    for config_path in locations:
        for config_file in ('production.ini', 'development.ini'):
            cfg = os.path.join(os.path.abspath(config_path), config_file)
            if os.path.isfile(cfg):
                return cfg
    return None


def daemon():
    def die_in_a_fire(signum, stack):
        for thread in threads:
            thread.kill()

    import signal
    from daemon import DaemonContext
    try:
        from daemon.pidfile import TimeoutPIDLockFile as PIDLockFile
    except:
        from daemon.pidlockfile import PIDLockFile

    config = appconfig("config:" + find_config_file())

    #pidlock = PIDLockFile('/var/run/fedoracommunity/worker.pid')
    #output = file('/var/log/fedoracommunity/worker.log', 'a')
    pidlock = PIDLockFile(
        config.get('cache-worker.pidfile', '/tmp/fedoracommunity-worker.pid')
    )
    output = file(
        config.get('cache-worker.logfile', '/tmp/fedoracommunity-worker.log'),
        'a')

    daemon = DaemonContext(pidfile=pidlock, stdout=output, stderr=output)
    daemon.terminate = die_in_a_fire

    n = int(config.get('cache-worker.threads', '8'))
    with daemon:
        log.info("Creating %i threads" % n)
        for i in range(n):
            threads.append(Thread())

        for thread in threads:
            thread.start()

        # I used to do thread.join() here, but that makes it so the
        # signal_handler never gets fired.  Crazy python...
        while any([not thread.die for thread in threads]):
            time.sleep(2)


def foreground():
    t = Thread()
    t.run()


def main():
    logging.basicConfig(
        level=logging.DEBUG,
        stream=sys.stdout,
    )
    if '--daemon' in sys.argv:
        daemon()
    else:
        foreground()
