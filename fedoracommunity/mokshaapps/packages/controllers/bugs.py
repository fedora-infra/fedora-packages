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

from tg import expose, tmpl_context

from moksha.lib.base import Controller
from moksha.lib.helpers import Category
from moksha.lib.helpers import Widget
from moksha.api.widgets import Grid, ContextAwareWidget
from moksha.api.connectors import get_connector

from helpers import PackagesDashboardContainer

class BugStatsWidget(ContextAwareWidget):
    template='mako:fedoracommunity.mokshaapps.packages.templates.bugs_stats_widget'
    params = ['id', 'product', 'package', 'version', 'num_closed',
              'num_open', 'num_new', 'num_new_this_week', 'num_closed_this_week']
    product = 'Fedora'
    version = 'rawhide'
    package = None
    num_closed = num_open = num_new = '-'
    num_new_this_week = num_closed_this_week = ''

bug_stats_widget = BugStatsWidget('bug_stats')


class BugsGrid(Grid):
    template='mako:fedoracommunity.mokshaapps.packages.templates.bugs_table_widget'
    resource = 'bugzilla'
    resource_path = 'query_bugs'

    def update_params(self, d):
        pkgdb = get_connector('pkgdb')

        collections = pkgdb.get_collection_table(active_only=True)
        releases = []
        for id, collection in collections.items():
            name = collection['name']
            ver = collection['version']
            label = "%s %s" % (name, ver)
            value = str(ver)
            if ver == 'devel':
                name = 'Rawhide'
                ver = 9999999
                label = 'Rawhide'
                value = 'rawhide'

            if name in ('Fedora', 'Rawhide', 'Fedora EPEL'):
                releases.append({'label': label, 'value': value, 'version': ver})

        def _sort(a,b):
            return cmp(int(b['version']), int(a['version']))

        releases.sort(_sort)

        d['release_table'] = releases

        super(BugsGrid, self).update_params(d)

bugs_grid = BugsGrid('bugs_grid')

class BugsDashboard(PackagesDashboardContainer):
    layout = [Category('content-col-apps',[
                         Widget('Bugs Dashboard', bug_stats_widget,
                                params={'package': '', 'filters':{'package': ''}}),
                         Widget('Recently Filed Bugs',
                                bugs_grid,
                                params={'filters':{'package': ''},
                                        'numericPager': True}),
                         ])]

bugs_dashboard = BugsDashboard('bugs_dashboard')


class BugsController(Controller):

    @expose('mako:moksha.templates.widget')
    def index(self, package):
        tmpl_context.widget = bugs_dashboard
        return {'options': {'package': package}}
