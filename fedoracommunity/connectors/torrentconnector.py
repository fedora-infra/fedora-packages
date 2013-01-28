# This file is part of Fedora Community.
# Copyright (C) 2008-2010  Red Hat, Inc.
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
:mod:`fedoracommunity.connectors.torrentconnector` - Fedora bittorrent connector
=======================================================================

This Connector works with the jsonconnector 

.. moduleauthor:: Seth Vidal <skvidal@fedoraproject.org>
"""

from datetime import datetime, timedelta
from moksha.common.lib.helpers import defaultdict
from jsonconnector import SimpleJsonConnector
from operator import itemgetter
import logging
from tg import config
log = logging.getLogger(__name__)

class TorrentConnector(SimpleJsonConnector):
    _method_paths = {}
    _query_paths = {}

    def __init__(self, environ=None, request=None):
        log.info('Torrent Connector initialized(%s)' % locals())                        
        super(TorrentConnector, self).__init__(environ, request)

    @classmethod
    def register(cls):
        cls.stats_url = config.get('fedoracommunity.connector.torrent.statsurl',
                    'http://torrent.fedoraproject.org/stats/current-stats.json')
        cls.register_query_most_active_torrents()
        cls.register_query_most_downloaded_torrents()
        
    @classmethod
    def register_query_most_active_torrents(cls):
        path = cls.register_query(
            'query_most_active_torrents',
            cls.query_most_active_torrents,
            primary_key_col = 'torrent_name',
            default_sort_col = 'number_of_downloaders',
            default_sort_order = -1,
            can_paginate = True)

        path.register_column('torrent_name',
                             default_visible = True,
                             can_sort = False,
                             can_filter_wildcards = False)

        path.register_column('number_of_downloaders',
                             default_visible = True,
                             can_sort = False,
                             can_filter_wildcards = False)


    def query_most_active_torrents(self, start_row=0,
                                rows_per_page=10,
                                order=1,
                                sort_col=None,
                                filters=None,
                                **params):
       
        torrents = self.call(self.stats_url)
        

        most_downloaders = sorted(torrents,key=itemgetter('downloaders'),
                                  reverse=True)

        results = []
        for torrent in most_downloaders:
            results.append({'number_of_downloaders': torrent['downloaders'], 
                            'torrent_name': torrent['name']})


        return (len(results), results[start_row:start_row+rows_per_page])

    @classmethod
    def register_query_most_downloaded_torrents(cls):
        path = cls.register_query(
            'query_most_downloaded_torrents',
            cls.query_most_downloaded_torrents,
            primary_key_col = 'torrent_name',
            default_sort_col = 'number_of_completed',
            default_sort_order = -1,
            can_paginate = True)

        path.register_column('torrent_name',
                             default_visible = True,
                             can_sort = False,
                             can_filter_wildcards = False)

        path.register_column('number_of_completed',
                             default_visible = True,
                             can_sort = False,
                             can_filter_wildcards = False)


    def query_most_downloaded_torrents(self, start_row=0,
                                rows_per_page=10,
                                order=1,
                                sort_col=None,
                                filters=None,
                                **params):
        log.info('most_downloaded_torrents called(%s)' % locals())                
        torrents = self.call(self.stats_url)

        most_downloaded = sorted(torrents,key=itemgetter('completed'),
                                  reverse=True)

        results = []
        for torrent in most_downloaded:
            results.append({'number_of_completed': torrent['completed'], 
                            'torrent_name': torrent['name']})


        return (len(results), results[start_row:start_row+rows_per_page])

    def query_most_active_torrents_history(self, torrent_count=10, **params):
        
        # obviously this is garbage data - just playing with flotwidget
        # line graphs
        flot_data = {}
        flot_data['data'] = []
        flot_data['options'] = {}
        flot_data['options']['legend'] = { 'show': True, 
                                          'noColumns': '1',}

        flot_data['data'].append({
            # data sets should be [timestamp, downloaders]
            'data': [[1, 1], [2,2], [3,3], [4,5], [5, 6]],
            'lines': {'show': True},
            'points': {'show': True},
            'label': 'Torrent1',
        })
        flot_data['data'].append({
            'data': [[2, 10], [3,23], [4,10], [5,8]],
            'lines': {'show': True},
            'points': {'show': True},            
            'label': 'Torrent2',
        })
        

        return flot_data
