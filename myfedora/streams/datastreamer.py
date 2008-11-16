# Copyright (C) 2008  Red Hat, Inc. All rights reserved.
#
# This copyrighted material is made available to anyone wishing to use, modify,
# copy, or redistribute it subject to the terms and conditions of the GNU
# General Public License v.2.  This program is distributed in the hope that it
# will be useful, but WITHOUT ANY WARRANTY expressed or implied, including the
# implied warranties of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.  You should have
# received a copy of the GNU General Public License along with this program; if
# not, write to the Free Software Foundation, Inc., 51 Franklin Street, Fifth
# Floor, Boston, MA 02110-1301, USA. Any Red Hat trademarks that are
# incorporated in the source code or documentation are not subject to the GNU
# General Public License and may only be used or replicated with the express
# permission of Red Hat, Inc.
#
# Author(s): Luke Macken <lmacken@redhat.com>

#from __future__ import with_statement

import re
import time
import cjson
import pylons
import logging
import threading
import pkg_resources

from tw.api import Widget
from pylons import request, config
from datetime import datetime
from pyorbited.simple import Client

log = logging.getLogger(__name__)


class Feed(object):
    """ A powerful Feed object.

    A Feed is initialized with an id and a url, and automatically handles the
    fetching, parsing, and caching of the data.

    """
    def __init__(self, id, url, *args, **kw):
        self.url = url
        self.id = id
        self.name = id # eventually figure out the name from the feed

    def iterentries(self):
        entries = pylons.g.feed_cache.fetch(self.url).entries
        for i, entry in enumerate(entries):
            entry['uid'] = '%s_%d' % (self.id, i)
            yield entry

    @property
    def entries(self):
        return [entry for entry in self.iterentries()]

    @property
    def num_entries(self):
        return len(self.entries)


class FeedWidget(Widget):
    params = {
            'entries': 'A list of feed entries',
            'charcount': 'The number of characters to display per entry',
    }
    template = 'genshi:myfedora.widgets.templates.feedhome'

    def update_params(self, d):
        super(Feed, self).update_params(d)
        limit = d.get('show')
        if limit:
            log.debug('show = %r' % limit)
            d['entries'] = []
            for i, entry in enumerate(self.entries):
                if i >= limit:
                    break
                d['entries'].append(entry)
        else:
            d['entries'] = self.entries


#
# Feed aggregation and caching
#

from Queue import Queue
from feedcache.cache import Cache

MAX_THREADS = 5

class FeedFetcher(threading.Thread):

    def __init__(self, storage, input_queue, output_queue):
        super(FeedFetcher, self).__init__()
        self.cache = Cache(storage)
        self.input_queue = input_queue
        self.output_queue = output_queue

    def run(self):
        print "Running FeedFetcher thread!"
        while True:
            next_url = self.input_queue.get()
            if next_url is None: # None causes thread to exit
                self.input_queue.task_done()
                break
            feed_data = self.cache.fetch(next_url)
            for entry in feed_data.entries:
                self.output_queue.put((feed_data.feed, entry))
            self.input_queue.task_done()
        print "FeedFetcher thread complete"


class FeedAggregator(threading.Thread):

    url_queue = Queue()

    feeds = {} # potentially useless?

    def __init__(self):
        super(FeedAggregator, self).__init__()
        self.load_feed_entry_points()

    def load_feed_entry_points(self):
        """ Load all data feeds from the 'moksha.feed' entrypoint """
        for plugin in pkg_resources.iter_entry_points('moksha.feed'):
            feed = plugin.load()()
            print "Loading %s feed" % feed.url
            self.url_queue.put(feed.url)
            self.feeds[feed.url] = feed
        # TODO: look at the 'feeds' propery on our widgets/apps?

    def run(self):
        print "Running FeedAggregator thread"
        num_threads = min(len(self.feeds), MAX_THREADS)
        print "Using %d threads" % num_threads
        for i in range(num_threads):
            self.url_queue.put(None)

        entry_queue = Queue()
        try:
            workers = []
            for i in range(num_threads):
                fetcher = FeedFetcher(config['app_globals'].feed_storage,
                                      self.url_queue, entry_queue)
                workers.append(fetcher)
                fetcher.setDaemon(True)
                fetcher.start()

            print "url_queue.join()"
            self.url_queue.join()

            print "joining on workers"
            for worker in workers:
                worker.join()

            # this requires the print thread
            # print "joining on entry_queue"
            # entry_queue.join()

        finally:
            storage.close()

        print "Results:"
        while True:
            feed, entry = entry_queue.get()
            if feed is None:
                entry_queue.task_done()
                break
            print "%s: %s" % (feed.title, entry.title)
            entry_queue.task_done()

        print "Done with thread!"


# TODO: Port this to the latest Orbited, and utilize Qpid for messaging.
class DataStreamer(threading.Thread):
    """ Our comet data streamer.

    This thread is responsible for periodically polling the data streams
    and sending events to our Orbited server.  This server then publishes
    this data to all of the subscribed users.

    TODO:
    - How do we unsubscribe users ?
    - Periodically refresh our plugin data sources,
      adding/removing as necessary.
    """
    streams = {} # {'stream name': DataStream instance}
    users = {} # {'stream name': [('user', session #),]}
    lock = threading.Lock() # Used for join requests

    def load_data_streams(self):
        """ Load the widget data streams.

        This loads all data sources from the myfedora.datastreams entry point
        as well as any 'data' properties on the widgets themselves.
        """
        for plugin in pkg_resources.iter_entry_points('myfedora.datastreams'):
            if not self.streams.has_key(plugin.name):
                print "Loading %s data stream" % plugin.name
                self.streams[plugin.name] = plugin.load()()
                self.users[plugin.name] = []
        for plugin in pkg_resources.iter_entry_points('myfedora.widgets'):
            if hasattr(plugin.load(), 'data'):
                if not self.streams.has_key(plugin.name):
                    print "Loading %s data stream" % plugin.name
                    self.streams[plugin.name] = plugin.load().data()
                    print self.streams[plugin.name]
                    self.users[plugin.name] = []
                else:
                    print "Already loaded", plugin.name

    def run(self):
        print "Running DataStreamer thread"
        self.load_data_streams()
        self.orbited = Client()
        self.orbited.connect()
        while True:
            for name, feed in self.streams.items():
                subscribers = self.user_keys(name)
                if subscribers:
                    print "Publishing data streams"
                    feed.refresh()
                    for item in feed:
                        # The last argument to this event method is whether
                        # or not to automatically convert the item to json.
                        # orbited uses a JSON converter that is bad at unicode,
                        # so we'll do it ourselves for now...
                        item = cjson.encode([item,])
                        print "sending %s to %s" % (repr(item), subscribers)
                        self.orbited.event(subscribers, item, False)

            # We don't want to poll as fast as we can, but we also don't
            # want to sleep for too long.
            # TODO: Make this suck less.
            time.sleep(10)

    #def user_keys(self, feed):
    #    with self.lock:
    #        return ['%s, %s, /feed/%s' % (user, session, feed) for
    #                user, session in self.users[feed]]

    #def join(self, user, feed, session='0'):
    #    print "%s joining %s feed (%s)" % (user, feed, session)
    #    with self.lock:
    #        if self.users.has_key(feed):
    #            if (user, session) not in self.users[feed]:
    #                self.users[feed].append((user, session))
    #        else:
    #            raise DataStreamerException("Cannot find feed: %s" % feed)


if __name__ == '__main__':
    f = FeedAggregator()
    f.start()
    f.join()
    print "Done!"
