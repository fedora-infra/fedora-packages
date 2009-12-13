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

from pylons import cache
from datetime import datetime, timedelta
from moksha.api.widgets import Grid
from moksha.api.widgets.containers import DashboardContainer
from moksha.lib.helpers import Category, Widget as MokshaWidget, defaultdict
from moksha.api.connectors import get_connector
from fedoracommunity.widgets.flot import FlotWidget

class MostActiveTorrents(Grid):
    template = 'mako:fedoracommunity.mokshaapps.statistics.templates.most_active_torrents'
    resource = 'torrent'
    resource_path='query_most_active_torrents'
    numericPager = True


most_active_torrent = MostActiveTorrents('most_active_torrents')

class MostDownloadedTorrents(Grid):
    template = 'mako:fedoracommunity.mokshaapps.statistics.templates.most_downloaded_torrents'
    resource = 'torrent'
    resource_path='query_most_downloaded_torrents'
    numericPager = True

most_downloaded_torrent = MostDownloadedTorrents('most_downloaded_torrents')



class MostActiveTorrentsChart(FlotWidget):
    """show the history of the most active torrents and their  activity
       for however long we have in the backend"""
    def update_params(self, d):
        torrent_connector = get_connector('torrent')
        torrent_cache = cache.get_cache('torrent')
        stats = torrent_cache.get_value(key='torrent_stats',
                createfunc=torrent_connector.query_most_active_torrents_history,
                expiretime=3600)
        d.data = stats['data']
        d.options = stats['options']
        super(MostActiveTorrentsChart, self).update_params(d)


most_active_torrents_chart = MostActiveTorrentsChart('most_active_torrents_chart')


class TorrentStatisticsDashboard(DashboardContainer):
    layout = [
            Category('left-content-column-apps', [
                MokshaWidget('Most active torrent', most_active_torrent),
                MokshaWidget('Most downloaded torrent', most_downloaded_torrent),
#                MokshaWidget('Most active torrents chart', most_active_torrents_chart),
                ]),
    ]

torrent_stats_dashboard = TorrentStatisticsDashboard('torrent_stats')
