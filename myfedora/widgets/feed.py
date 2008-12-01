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

import pylons

from tw.api import Widget
from myfedora.lib.utils import fullurl

class Feed(Widget):
    """ A powerful Feed object.

    A Feed is initialized with an id and a url, and automatically handles the
    fetching, parsing, and caching of the data.

    Ways of creating utilizing the Feed widget:

       1) Subclassing

          class MyFeed(Feed):
              url = 'http://foo.bar/feed.xml'

          myfeed = MyFeed()
          myfeed() # renders the widget, usually done in the template

       2) As ToscaWidget children

          class MyWidget(Widget):
              myfeedurl = 'http://foo.bar/feed.xml'
              children = [Feed('myfeed', url=myfeedurl)]
              template = "${c.myfeed()}"

        3) As a generator

            feed = Feed(url='http://foo.bar/feed.xml')
            for entry in feed.iterentries():
                print entry.title

    """
    template = 'mako:/myfedora/widgets/templates/feed_home.html'
    params = {
            'name': 'The name of this feed',
            'link': 'The url to the site that this feed is for',
            'entries': 'A list of feed entries',
    }

    def __new__(cls, *args, **kw):
        """ If we're instantiated with a specific view, then use the 
        appropriate template 
        Available views: home, canvas, profile
        """
        view = kw.get('view', False)
        if not view:
            view = getattr(cls, 'view', False)
        if view:
            class AlternateFeedView(cls):
                template = 'mako:/myfedora/widgets/templates/feed_%s.html' % view
            return super(Feed, cls).__new__(AlternateFeedView, *args, **kw)
        return super(Feed, cls).__new__(cls, *args, **kw)

    def _get_full_url(self):
        if self.url.startswith('/'):
            feed_url = fullurl(self.url)
        else:
            feed_url = self.url
        return feed_url

    def iterentries(self, d=None):
        url = self._get_full_url()
        feed = pylons.g.feed_cache.fetch(url)
        if d:
            d['link'] = feed.feed.link
            d['title'] = feed.feed.title
        for i, entry in enumerate(feed.entries):
            entry['uid'] = '%s_%d' % (self.id, i)
            yield entry

    @property
    def num_entries(self):
        return len(self.entries)

    def update_params(self, d):
        super(Feed, self).update_params(d)
        d['entries'] = []
        limit = d.get('show')
        if limit:
            for i, entry in enumerate(self.iterentries(d)):
                if i >= limit:
                    break
                d['entries'].append(entry)
        else:
            for entry in self.iterentries():
                d['entries'].append(entry)
