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

from moksha.lib.base import Controller
from moksha.lib.helpers import (Category, MokshaApp, not_anonymous,
                                param_has_value, param_contains, Any, Not)
from moksha.api.widgets.containers import DashboardContainer
from moksha.api.widgets import Grid, ContextAwareWidget

from tg import expose, tmpl_context

class SearchContainer(DashboardContainer, ContextAwareWidget):
    template = 'mako:fedoracommunity.mokshaapps.searchresource.templates.searchcontainer'
    params=['search']
    layout = [Category('content-column',
                       [MokshaApp('Package Search', 'fedoracommunity.search/xapian_packages',
                                  params={'search': ''}
                                 )
                        ])
              ]

class PkgdbSearchGrid(Grid):
    template="mako:fedoracommunity.mokshaapps.searchresource.templates.pkgdbsearchgrid"
    resource = 'pkgdb'
    resource_path = 'search_packages'
    numericPager = True

class YumSearchGrid(Grid):
    template="mako:fedoracommunity.mokshaapps.searchresource.templates.pkgdbsearchgrid"
    resource = 'yum'
    resource_path = 'search_packages'
    numericPager = True

class PeopleSearchGrid(Grid):
    template="mako:fedoracommunity.mokshaapps.searchresource.templates.peoplesearchgrid"
    resource = 'fas'
    resource_path = 'search_people'
    numericPager = True

class XapianSearchGrid(Grid):
    template="mako:fedoracommunity.mokshaapps.searchresource.templates.pkgdbsearchgrid"
    resource = 'xapian'
    resource_path = 'search_packages'
    numericPager = True

search_container = SearchContainer('search')
yum_search_grid = YumSearchGrid('yum_search')
pkgdb_search_grid = PkgdbSearchGrid('pkgdb_grid')
people_search_grid = PeopleSearchGrid('people_grid')
xapian_search_grid = XapianSearchGrid('xapian_grid')

class RootController(Controller):

    @expose('mako:moksha.templates.widget')
    def index(self, **kwds):
        options = {'search': '',
                   'people_checked': '',
                   'packages_checked':''
                   }

        tmpl_context.widget = search_container
        search = kwds.get('search')
        search_types = kwds.get('st', ['people', 'packages'])

        if 'people' in search_types:
            options['people_checked']='checked="checked"'

        if 'packages' in search_types:
            options['packages_checked']='checked="checked"'

        if search:
            options['search'] = search

        return {'options': options}

    @expose('mako:moksha.templates.widget')
    def people(self, **kwds):

        search = kwds.get('search',kwds.get('s'))

        options= {'filters':{'search': search}}

        tmpl_context.widget = people_search_grid

        return {'options': options}

    @expose('mako:moksha.templates.widget')
    def packages(self, **kwds):

        search = kwds.get('search',kwds.get('s'))
        options= {'filters':{'search': search}}

        tmpl_context.widget = pkgdb_search_grid

        return {'options': options}

    @expose('mako:moksha.templates.widget')
    def yum_packages(self, **kwds):

        search = kwds.get('search',kwds.get('s'))
        options= {'filters':{'search': search}}

        tmpl_context.widget = yum_search_grid

        return {'options': options}

    @expose('mako:moksha.templates.widget')
    def xapian_packages(self, **kwds):

        search = kwds.get('search',kwds.get('s'))
        options= {'filters':{'search': search}}

        tmpl_context.widget = xapian_search_grid

        return {'options': options}





