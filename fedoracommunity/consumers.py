import os
import json
import time

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
from fedoracommunity.search import utils
from fedoracommunity.pool import ThreadPool

import logging
log = logging.getLogger("fedmsg")


class FakeTG2Request(object):
    environ = {}


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


def make_kwargs(connector, path, info, filters, op):

    if op == 'method':
        # No pagination args for method calls, and no envelope
        return (connector, '', None,), filters

    # Otherwise, we're dealing with a 'query' op, and it looks like this
    kwargs = dict(
        start_row=0,
        rows_per_page=10,
        filters=filters
    )
    if hasattr(connector, 'get_default_sort_col'):
        kwargs['sort_col'] = connector.get_default_sort_col(path)
    if hasattr(connector, 'get_default_sort_order'):
        kwargs['order'] = connector.get_default_sort_order(path)
    return (connector,), kwargs


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

        self.cache_path = config.get(
            'fedoracommunity.connector.xapian.package-search.db',
            'xapian').strip('search')
        self.tagger_url = config.get(
            'fedoracommunity.connector.tagger.baseurl',
            'https://apps.fedoraproject.org/tagger')
        self.mdapi_url = config.get(
            'fedoracommunity.connector.mdapi.baseurl',
            'https://apps.fedoraproject.org/mdapi')
        # TODO - this can be removed.
        self.pkgdb_url = config.get(
            'fedoracommunity.connector.pkgdb.baseurl',
            'https://admin.fedoraproject.org/pkgdb')
        self.icons_url = config.get(
            'fedoracommunity.connector.icons.baseurl',
            'https://alt.fedoraproject.org/pub/alt/screenshots')

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
        self.update_xapian(msg)
        self.update_caches(msg)

    def update_caches(self, msg):
        for conn_name, connector in self.connectors.items():
            for path, info in connector._cache_prompts.items():

                matches = info['prompt'](msg)
                if matches is None:
                    continue
                matches = list(matches)
                if not matches:
                    continue

                fn = info['fn']
                op = info['op']
                namespace = info['namespace']

                generator = generator_factory(namespace, fn)
                def clear_and_refresh_items(filters):
                    args, kw = make_kwargs(connector, path, info, filters, op)
                    lookup_key = generator(*args[1:], **kw)
                    hashed_key = mangler(lookup_key)
                    log.info("Refreshing %s" % lookup_key)
                    # Destroy the old value
                    self.mc.delete(hashed_key)
                    # Run the connector to re-fill the cache.
                    try:
                        fn(*args, **kw)
                        log.info(" Done with %s" % hashed_key)
                    except Exception as e:
                        # Log a warning, but don't email us...
                        log.warning(str(e))

                log.info("Found %r matches..." % len(matches))
                pool = ThreadPool(min([len(matches), 20]))
                list(pool.map(clear_and_refresh_items, matches))

    def update_xapian(self, msg):

        # TODO - this needs to be rethought to figure out *when* to update the
        # fedora-packages xapian cache.  It used to happen anytime anything
        # changed in pkgdb, but when is a new good event?  Yash - you don't
        # have to modify this function (in the beginning).  Save it for last.

        # If any number of different pkgdb things happen to a package, let's
        # just update and not care too much about whatever it was that just
        # happened.
        if '.pkgdb.' not in msg['topic']:
            return

        # This one is spammy
        if '.pkgdb.acl.update' in msg['topic']:
            return

        # We'll take all others, so long as they have these fields.
        if 'package_listing' in msg['msg']:
            name = msg['msg']['package_listing']['package']['name']
        elif 'package' in msg['msg']:
            name = msg['msg']['package']['name']
        else:
            # If the message doesn't have either of those two, then give up.
            return

        log.info("Considering xapian index updates for %r" % name)

        indexer = self.try_real_hard_to_get_the_xapian_indexer()

        try:
            indexer.pull_icons()
            indexer.cache_icons()
        except Exception as e:
            log.warn("Failed to cache icons %r" % e)

        try:
            package = indexer.construct_package_dictionary(dict(name=name))

            if package is None:
                log.warn("Unable to construct xapian pkg dict for %r" % name)
                return

            document = indexer._create_document(package)
            processed = indexer._process_document(package, document)

            old_document = self._get_old_document(name)
            if old_document:
                docid = old_document.get_docid()
                log.debug('Deleting old document %r.' % docid)
                indexer.indexer.delete(xapid=docid)

            indexer.indexer.add(processed)
            log.info("Done adding new document %r" % name)
        finally:
            indexer.indexer.close()

    def _get_old_document(self, package_name):
        search_name = utils.filter_search_string(package_name)
        search_string = "%s EX__%s__EX" % (search_name, search_name)
        matches = self._xapian_connector().do_search(search_string, 0, 10)

        for match in matches:
            result = json.loads(match.document.get_data())
            if result['name'] == package_name:
                return match.document

        return None

    def _xapian_connector(self):
        request = FakeTG2Request()
        for conn_entry in pkg_resources.iter_entry_points('fcomm.connector'):
            if conn_entry.name == 'xapian':
                cls = conn_entry.load()
                cls.register()
                return cls(request.environ, request)

        raise ValueError("No Xapian connector could be found.")

    def try_real_hard_to_get_the_xapian_indexer(self):
        """ Try over and over again to get a lock on the xapian indexer.

        We may end up trying forever, in which case our inbound queue will fill
        up, nagios will alert, and then a human being will come and restart us.
        """
        import xapian
        from fedoracommunity.search import index
        interval = 0.5
        indexer = None
        while indexer is None:
            try:
                indexer = index.Indexer(
                    cache_path=self.cache_path,
                    tagger_url=self.tagger_url,
                    # TODO - this can be removed.  Make sure to remove it from the source of index.Indexer too.
                    pkgdb_url=self.pkgdb_url,
                    mdapi_url=self.mdapi_url,
                    icons_url=self.icons_url,
                )
            except xapian.DatabaseLockError as e:
                log.warn(str(e))
                log.info("Trying again in %f seconds." % interval)
                time.sleep(interval)
        return indexer
