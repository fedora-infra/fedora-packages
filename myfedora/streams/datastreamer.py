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

from __future__ import with_statement

import time
import cjson
import threading
import pkg_resources

from pyorbited.simple import Client


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

    def user_keys(self, feed):
        with self.lock:
            return ['%s, %s, /feed/%s' % (user, session, feed) for
                    user, session in self.users[feed]]

    def join(self, user, feed, session='0'):
        print "%s joining %s feed (%s)" % (user, feed, session)
        with self.lock:
            if self.users.has_key(feed):
                if (user, session) not in self.users[feed]:
                    self.users[feed].append((user, session))
            else:
                raise DataStreamerException("Cannot find feed: %s" % feed)
