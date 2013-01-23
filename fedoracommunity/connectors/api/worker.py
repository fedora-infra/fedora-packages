#!/usr/bin/env python
""" This is a long-running worker process that generates values asychronously
for dogpile.cache and the fcomm_connector api.

It should be run under a sysvinit script as a daemon.  It should be run as 8 or
so threads.
"""

import tg
import os
import json
import time
import types
import retask.queue
import memcache

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

def main():
    if queue.length == 0:
        print("No tasks found in the queue.  Sleeping for 2 seconds.")
        return

    task = queue.dequeue()
    data = json.loads(task.data)

    mc = memcache.Client(data['memcached_addrs'])

    try:
        # Here are those three attribute that we hung on the original cached f
        name = data['fn']['name']
        path = data['fn']['path']
        typ = data['fn']['type']

        conn_cls = mw_obj._connectors[name]['connector_class']
        conn_obj = conn_cls({}, object())
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


while True:
    try:
        main()
    except KeyboardInterrupt:
        break
    except Exception:
        import traceback
        traceback.print_exc()
    time.sleep(2)

