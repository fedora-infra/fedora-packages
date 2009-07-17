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
:mod:`fedoracommunity.streams.wikistream` - Fedora Wiki Stream
==============================================================

This set of PollingDataStreams works with the MediaWiki API of the Fedora
Project wiki.

.. moduleauthor:: Ian Weller <iweller@redhat.com>
"""

from fedora.client.wiki import Wiki
from datetime import timedelta, datetime
from beaker.cache import Cache
from moksha.api.streams import PollingDataStream
import logging

log = logging.getLogger(__name__)

class AllRevisionsDataStream(PollingDataStream):
    frequency = timedelta(hours=12)

    def poll(self):
        c = Cache('wiki')
        w = Wiki()
        try:
            data = c.get_value(key='all_revisions')
        except KeyError:
            # we haven't gotten any data yet.
            data = {'revs': {}, 'last_rev_checked': 0}
        starttime = datetime.now()
        data['revs'].update(w.fetch_all_revisions(
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
        c.set_value(key='all_revisions', value=data)
        log.info("Cached wiki revisions, took %s" % \
                 (datetime.now() - starttime))
        return True
