from moksha.lib.base import Controller
from moksha.lib.helpers import (Category, MokshaApp, Not, not_anonymous,
                               MokshaWidget, param_has_value)
from moksha.api.widgets.containers import DashboardContainer
from tg import expose, tmpl_context

class SearchContainer(DashboardContainer):
    template = 'mako:fedoracommunity.mokshaapps.searchresource.templates.searchcontainer'
    layout = [Category('content-column',
                       [MokshaApp('Package Search', 'fedoracommunity.search/packages',
                                  params={'search': None},
                                  auth=param_has_value('search')),
                        MokshaApp('People Search','fedoracommunity.search/people',
                                  params={'search': None},
                                  auth=[not_anonymous(), param_has_value('search')])
                        ])
              ]

search_container = SearchContainer('search')

class RootController(Controller):

    @expose('mako:moksha.templates.widget')
    def index(self, **kwds):
        tmpl_context.widget = search_container
        search = kwds.get('search',kwds.get('s',''))

        return {'options':{'search': search}}

    @expose('mako:fedoracommunity.mokshaapps.searchresource.templates.packages')
    def packages(self, **kwds):
        search = kwds.get('search',kwds.get('s'))


