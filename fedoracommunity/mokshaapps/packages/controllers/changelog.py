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
from moksha.lib.helpers import Category, Widget
from moksha.api.widgets import ContextAwareWidget, Grid

from helpers import PackagesDashboardContainer
from links import changelog_links

class ChangelogGrid(ContextAwareWidget, Grid):
    template='mako:fedoracommunity.mokshaapps.packages.templates.changelog_table_widget'

    def update_params(self, d):
        d['resource'] = 'koji',
        d['resource_path'] = 'query_changelogs'
        super(ChangelogGrid, self).update_params(d)

changelog_grid = ChangelogGrid('changelog_table')

class ChangelogDashboard(PackagesDashboardContainer):
    template = 'mako:fedoracommunity.mokshaapps.packages.templates.single_col_dashboard'
    layout = [Category('content-col-apps',[
                          Widget('Latest Build Changelogs',
                                 changelog_grid,
                                 params={'filters':{'package': ''},
                                         'numericPager':True})
                       ])]

changelog_dashboard = ChangelogDashboard('changelog_dashboard')

class ChangelogController(Controller):
    @expose('mako:moksha.templates.widget')
    def index(self, package):
        tmpl_context.widget = changelog_dashboard
        return {'options':{'package': package}}

    @expose('mako:moksha.templates.widget')
    def table(self, filters, more_link_code):
        tmpl_context.widget = changelog_grid

        more_link = None
        numericPager = False
        if more_link_code:
            more_link = changelog_links.get_data(more_link_code)
        else:
            numericPager = True

        return {'options':{'filters': filters, 'more_link': more_link, 'numericPager': numericPager}}
