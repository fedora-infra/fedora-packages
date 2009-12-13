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
from fedora.client import Wiki
from datetime import datetime, timedelta
from moksha.api.widgets import Grid
from moksha.api.widgets.containers import DashboardContainer
from moksha.lib.helpers import Category, Widget as MokshaWidget, defaultdict
from moksha.api.connectors import get_connector
from fedoracommunity.widgets.flot import FlotWidget
import json

class MostActiveWikiPages(Grid):
    template = 'mako:fedoracommunity.mokshaapps.statistics.templates.wiki_active_pages'
    resource = 'wiki'
    resource_path='query_most_active_pages'
    numericPager = True


most_active_wiki_pages = MostActiveWikiPages('most_active_wiki_pages')


class MostActiveWikiUsers(FlotWidget):
    def update_params(self, d):
        wiki_connector = get_connector('wiki')
        wiki_cache = cache.get_cache('wiki')
        stats = wiki_cache.get_value(key='most_active_wiki_users',
                createfunc=wiki_connector.query_most_active_users,
                expiretime=1800)
        d.data = stats['data']
        d.options = stats['options']
        super(MostActiveWikiUsers, self).update_params(d)


most_active_wiki_users = MostActiveWikiUsers('most_active_wiki_users')


class WikiEditsPerDay(FlotWidget):
    def update_params(self, d):
        wiki_connector = get_connector('wiki')
        wiki_cache = cache.get_cache('wiki')
        flot = wiki_cache.get_value(key='wiki_edits_per_day',
                createfunc=wiki_connector.flot_wiki_edits_per_day,
                expiretime=1800)
        if not flot:
            (d.data, d.options) = (False, False)
        else:
            (d.data, d.options) = (json.dumps(flot['data']), flot['options'])
        super(WikiEditsPerDay, self).update_params(d)


wiki_edits_per_day = WikiEditsPerDay('wiki_edits_per_day')


class WikiStatisticsDashboard(DashboardContainer):
    layout = [
            Category('left-content-column-apps', [
                MokshaWidget('Most active wiki pages', most_active_wiki_pages),
                MokshaWidget('Most active wiki users', most_active_wiki_users),
                MokshaWidget('Wiki edits per day', wiki_edits_per_day),
                ]),
    ]

wiki_stats_dashboard = WikiStatisticsDashboard('wiki_stats')
