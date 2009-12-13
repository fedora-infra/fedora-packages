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
:mod:`fedoracommunity.connectors.wikiconnector` - Fedora Wiki Connector
=======================================================================

This Connector works with the MediaWiki API of the Fedora Project wiki.

.. moduleauthor:: Ian Weller <iweller@redhat.com>
"""

from fedora.client import Wiki
from datetime import datetime, timedelta
from time import mktime
from pylons import cache, config
from shove import Shove
from moksha.connector import IConnector, ICall, IQuery, ParamFilter
from moksha.lib.helpers import defaultdict

class WikiConnector(IConnector, IQuery):
    _method_paths = {}
    _query_paths = {}

    def __init__(self, environ=None, request=None):
        super(WikiConnector, self).__init__(environ, request)

    def _get_recent_changes(self):
        now = datetime.utcnow()
        then = now - timedelta(days=7)
        wiki = Wiki()
        return wiki.get_recent_changes(now=now, then=then)

    @classmethod
    def register(cls):
        cls.register_query_most_active_pages()

    @classmethod
    def register_query_most_active_pages(cls):
        path = cls.register_query(
            'query_most_active_pages',
            cls.query_most_active_pages,
            primary_key_col = 'title',
            default_sort_col = 'number_of_edits',
            default_sort_order = -1,
            can_paginate = True)

        path.register_column('title',
                             default_visible = True,
                             can_sort = False,
                             can_filter_wildcards = False)

        path.register_column('number_of_edits',
                             default_visible = True,
                             can_sort = False,
                             can_filter_wildcards = False)

        path.register_column('last_edited_by',
                             default_visible = True,
                             can_sort = False,
                             can_filter_wildcards = False)

    def query_most_active_pages(self, start_row=0,
                                rows_per_page=10,
                                order=1,
                                sort_col=None,
                                filters=None,
                                **params):
        edit_counts = defaultdict(int) # {pagename: # of edits}
        last_edited_by = {} # {pagename: username}

        wiki_cache = cache.get_cache('wiki')
        changes = wiki_cache.get_value(key='recent_changes',
                                       createfunc=self._get_recent_changes,
                                       expiretime=3600)

        for change in changes:
            edit_counts[change['title']] += 1
            if change['title'] not in last_edited_by.keys():
                last_edited_by[change['title']] = change['user'].lower()

        most_active_pages = sorted(edit_counts.items(),
                                   cmp=lambda x, y : cmp(x[1], y[1]),
                                   reverse=True)

        page_data = []
        for i, page in enumerate(most_active_pages):
            page_data.append({'number_of_edits': page[1], 'title': page[0],
                              'last_edited_by': last_edited_by[page[0]]})

        return (len(page_data), page_data[start_row:start_row+rows_per_page])

    def query_most_active_users(self, user_count=10, **params):
        users = defaultdict(list)

        wiki_cache = cache.get_cache('wiki')
        changes = wiki_cache.get_value(key='recent_changes',
                                       createfunc=self._get_recent_changes,
                                       expiretime=3600)

        for change in changes:
            users[change['user'].lower()].append(change['title'])

        most_active_users = sorted(users.items(),
                cmp=lambda x, y: cmp(len(x[1]), len(y[1])),
                reverse=True)[:user_count]

        user_data = []
        user_ticks = []
        for i, user in enumerate(most_active_users):
            user_data.append([i, len(user[1])])
            user_ticks.append([i + 0.5, user[0]])

        flot_data = {'data': [], 'options': {'xaxis': {}}}
        flot_data['options']['xaxis']['ticks'] = user_ticks
        flot_data['data'].append({
            'data': user_data,
            'bars': {'show': True}
        })

        return flot_data

    def flot_wiki_edits_per_day(self, **params):
        stats_cache = Shove(config.get('stats_cache'))
        try:
            data = stats_cache['wiki_all_revisions']
        except KeyError:
            return False

        timestamps = defaultdict(int)
        for rev_id in data['revs']:
            timestamp = data['revs'][rev_id]['time']
            day_timestamp = int(mktime((timestamp[0], timestamp[1],
                                        timestamp[2], 0, 0, 0, 0, 0, 0))*1000)
            timestamps[day_timestamp] += 1

        flot = {'data': [], 'options': {'xaxis': {'mode': 'time'}}}
        timestamps_sorted = timestamps.keys()
        timestamps_sorted.sort()
        flot['data'] = [[[timestamp, timestamps[timestamp]] \
                         for timestamp in timestamps_sorted]]
        return flot
