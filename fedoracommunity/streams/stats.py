# This file is part of Fedora Community.
# Copyright (C) 2008-2009  Red Hat, Inc.
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
# 
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
:mod:`fedoracommunity.streams.stats` - Statistics Streams
==============================================================

This set of PollingDataStreams makes the backend behind the Statistics
application automatic.

.. moduleauthor:: Ian Weller <ian@ianweller.org>
"""

from fedora.client.wiki import Wiki
from moksha.api.streams import PollingDataStream
from shove import Shove
from pylons import config
from datetime import timedelta, datetime
from moksha.api.connectors import get_connector

class ClaDoneDataStream(PollingDataStream):
    frequency = timedelta(minutes=2)

    def poll(self):
        self.log.info("Cached cla_done graph")
        stats_cache = Shove(config.get('stats_cache'))
        fas_connector = get_connector('fas')
        data = fas_connector.group_membership_over_time()
        stats_cache['group_membership_cla_done'] = data
        return True


class WikiAllRevisionsDataStream(PollingDataStream):
    now = True
    frequency = timedelta(hours=12)

    def poll(self):
        stats_cache = Shove(config.get('stats_cache'))
        wiki = Wiki()
        try:
            data = stats_cache['all_revisions']
        except TypeError:
            # we haven't gotten any data yet.
            data = {'revs': {}, 'last_rev_checked': 0}
        starttime = datetime.now()
        self.log.info("Caching wiki revisions now... this could take a while")
        data['revs'].update(wiki.fetch_all_revisions(
                start = data['last_rev_checked']+1,
                flags = False,
                timestamp = True,
                user = True,
                size = False,
                comment = False,
                content = False,
                title = True,
                ignore_imported_revs = True,
        ))
        revids = data['revs'].keys()
        revids.sort()
        data['last_rev_checked'] = revids[-1]
        stats_cache['all_revisions'] = data
        self.log.info("Cached wiki revisions, took %s seconds" % \
                 (datetime.now() - starttime))
        return True
