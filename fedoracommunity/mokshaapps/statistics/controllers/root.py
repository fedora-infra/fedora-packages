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

from tg import expose, tmpl_context
from moksha.lib.base import Controller
from moksha.lib.helpers import Category, MokshaApp
from moksha.api.widgets.containers.dashboardcontainer import applist_widget

from fedoracommunity.widgets import SubTabbedContainer
from fedoracommunity.mokshaapps.statistics.widgets import *

class StatsNavContainer(SubTabbedContainer):
    params = ['applist_widget']
    applist_widget = applist_widget
    template='mako:fedoracommunity.mokshaapps.statistics.templates.stats_nav'
    tabs = (
        Category('', (
            MokshaApp('Wiki', 'fedoracommunity.statistics/wiki', params={}),
            MokshaApp('Accounts', 'fedoracommunity.statistics/fas', params={}),
            MokshaApp('Torrents', 'fedoracommunity.statistics/torrents', params={}),
            MokshaApp('Users', 'fedoracommunity.statistics/users', params={}),
            MokshaApp('Mirrors', 'fedoracommunity.statistics/mirrors', params={}),
            MokshaApp('Packages', 'fedoracommunity.statistics/packages', params={}),
            MokshaApp('Updates', 'fedoracommunity.statistics/updates', params={}),
            ),
        ),
    )

statistics_nav_container = StatsNavContainer('statistics_nav_container')


class RootController(Controller):

    @expose('mako:moksha.templates.widget')
    def index(self):
        tmpl_context.widget = statistics_nav_container
        return dict(options={})

    @expose('mako:moksha.templates.widget')
    def wiki(self):
        tmpl_context.widget = wiki_stats_dashboard
        return dict(options={})

    @expose('mako:moksha.templates.widget')
    def fas(self):
        tmpl_context.widget = fas_stats_dashboard
        return dict(options={})

    @expose('mako:moksha.templates.widget')
    def torrents(self):
        tmpl_context.widget = torrent_stats_dashboard
        return dict(options={})

    @expose('mako:moksha.templates.widget')
    def mirrors(self):
        tmpl_context.widget = mirror_stats_dashboard
        return dict(options={})

    @expose('mako:moksha.templates.widget')
    def users(self):
        tmpl_context.widget = user_stats_dashboard
        return dict(options={})

    @expose('mako:moksha.templates.widget')
    def packages(self):
        tmpl_context.widget = num_pkgs_per_collection
        return dict(options={})

    @expose('mako:fedoracommunity.mokshaapps.statistics.templates.updates')
    def updates(self, release=None, *args, **kw):
        tmpl_context.releases = release_downloads_filter
        tmpl_context.widget = all_updates_widget

        pkgdb_connector = get_connector('pkgdb')
        releases = pkgdb_connector.get_fedora_releases(rawhide=False)
        if not release:
            release = releases[0][0]

        bodhi_connector = get_connector('bodhi')
        data = bodhi_connector.get_metrics()

        collection = pkgdb_connector.get_collection_by_koji_name(release)
        if collection['branchname'] not in data:
            stripped = collection['branchname'].replace('-', '')
            if stripped in data:
                collection['branchname'] = stripped
            else:
                raise Exception("Cannot find metrics for %s" % collection['branchname'])

        release = collection['branchname']
        release_name = '%s %s' % (collection['name'], collection['version'])
        koji_name = collection['koji_name']

        return dict(default=koji_name, release=release, release_name=release_name,
                    data=data, options=releases)
