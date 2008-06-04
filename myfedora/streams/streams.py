
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

import re
import feedparser

from datetime import datetime, timedelta

class RSSDataStream(list):

    url = ''
    interval = timedelta(minutes=10)
    max_entries = 10

    def __init__(self):
        if not self.url:
            raise NotImplementedError("No RSS url specified!")
        self.last_change = datetime.utcnow()
        self.last_poll = datetime.utcnow()
        self.refresh(force=True)

    def refresh(self, force=False):
        if not force and (datetime.utcnow() - self.last_poll) < self.interval:
            return
        print "Refreshing data for %s" % self.url
        print "max_entries =", self.max_entries
        entries = []
        imgregex = re.compile('<img src="(.*)" alt="" />')
        feed = feedparser.parse(self.url)
        for entry in feed['entries'][:self.max_entries]:
            entries.append({
                'link'  : entry['link'],
                'title' : entry['title']
            })
            img = imgregex.match(entry['summary'])
            if img:
                entries[-1]['image'] = img.group(1)

        changes = True
        if len(self) == len(entries):
            for entry in range(0, len(entries) - 1):
                if entries[entry]['link'] != self[entry]['link']:
                    break
            changes = False
        if changes:
            self[:]
            self.extend(entries)
            self.last_change = datetime.utcnow()

        self.last_poll = datetime.utcnow()

    def __str__(self):
        return "<%s %s>" % (self.__class__.__name__, self.url)
