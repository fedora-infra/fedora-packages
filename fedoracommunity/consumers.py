import memcache
import pkg_resources

import tg

import fedmsg
import fedmsg.consumers


from paste.deploy import appconfig

from fedoracommunity.connectors.api.connector import (
    cache_key_generator as generator_factory,
    cache_key_mangler as mangler,
)
from fedoracommunity.connectors.api.worker import (
    find_config_file,
)

import logging
log = logging.getLogger("fedmsg")


class FakeTG2Request(object):
    environ = {}


def make_kwargs(connector, path, info, filters):
    kwargs = dict(
        start_row=0,
        rows_per_page=10,
        filters=filters,
    )
    if hasattr(connector, 'get_default_sort_col'):
        kwargs['sort_col'] = connector.get_default_sort_col(path)
    if hasattr(connector, 'get_default_sort_order'):
        kwargs['order'] = connector.get_default_sort_order(path)
    return kwargs



class CacheInvalidator(fedmsg.consumers.FedmsgConsumer):
    topic = '*'
    config_key = 'fedoracommunity.fedmsg.consumer.enabled'

    def __init__(self, hub, *args, **kwargs):

        config = appconfig("config:" + find_config_file())
        tg.config.update(config)

        url_key = 'cache.connectors.arguments.url'
        if url_key not in config:
            raise ValueError("%r not in config and is required.")
        self.mc = memcache.Client([config[url_key]])

        self._load_connectors()

        super(CacheInvalidator, self).__init__(hub, *args, **kwargs)

    def _load_connectors(self):
        self.connectors = {}
        request = FakeTG2Request()
        for conn_entry in pkg_resources.iter_entry_points('fcomm.connector'):
            log.info('Loading %s connector' % conn_entry.name)
            cls = conn_entry.load()
            cls.register()
            self.connectors[conn_entry.name] = cls(request.environ, request)

    def consume(self, msg):
        msg = msg['body']
        for conn_name, connector in self.connectors.items():
            for path, info in connector._cache_prompts.items():

                matches = info['prompt'](msg)
                if not matches:
                    continue

                fn = info['fn']
                namespace = info['namespace']

                generator = generator_factory(namespace, fn)
                for filters in matches:
                    args = (connector,)
                    kwargs = make_kwargs(connector, path, info, filters)
                    lookup_key = generator(**kwargs)
                    hashed_key = mangler(lookup_key)
                    log.info("Updating %s" % lookup_key)
                    log.debug("    hash %s" % hashed_key)
                    # Destroy the old value
                    self.mc.delete(hashed_key)
                    # Run the connector to re-fill the cache.
                    fn(*args, **kwargs)
