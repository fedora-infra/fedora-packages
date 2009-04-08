from moksha.lib.base import Controller
from moksha.lib.helpers import (Category, MokshaApp, Not, not_anonymous,
                               MokshaWidget, param_has_value)
from moksha.api.widgets.containers import DashboardContainer
from moksha.api.widgets import Grid

from tg import expose, tmpl_context

class SearchContainer(DashboardContainer):
    template = 'mako:fedoracommunity.mokshaapps.searchresource.templates.searchcontainer'
    params=['search']
    layout = [Category('content-column',
                       [MokshaApp('Package Search', 'fedoracommunity.search/packages',
                                  params={'search': None},
                                  auth=param_has_value('search')),
                        MokshaApp('People Search','fedoracommunity.search/people',
                                  params={'search': None},
                                  auth=[not_anonymous(), param_has_value('search')])
                        ])
              ]

class PkgdbSearchGrid(Grid):
    template="mako:fedoracommunity.mokshaapps.searchresource.templates.pkgdbsearchgrid"
    def update_params(self, d):
        d['resource'] = 'pkgdb'
        d['resource_path'] = 'search_packages'
        super(PkgdbSearchGrid, self).update_params(d)

class PeopleSearchGrid(Grid):
    template="mako:fedoracommunity.mokshaapps.searchresource.templates.peoplesearchgrid"
    def update_params(self, d):
        d['resource'] = 'fas'
        d['resource_path'] = 'search_people'
        super(PeopleSearchGrid, self).update_params(d)

search_container = SearchContainer('search')
pkgdb_search_grid = PkgdbSearchGrid('pkgdb_grid')
people_search_grid = PeopleSearchGrid('people_grid')

class RootController(Controller):

    @expose('mako:moksha.templates.widget')
    def index(self, **kwds):
        options = {'search': ''}
        tmpl_context.widget = search_container
        search = kwds.get('search')

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






