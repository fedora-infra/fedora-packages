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

from tg import expose, tmpl_context, validate, request
from tw.api import JSLink, Widget
from formencode import validators
from paste.deploy.converters import asbool

import simplejson as json

from moksha.lib.base import Controller
from moksha.lib.helpers import Category, MokshaApp, not_anonymous
from moksha.api.connectors import get_connector
from moksha.api.widgets import ContextAwareWidget, Grid
from moksha.api.widgets.containers import DashboardContainer
from moksha.api.widgets.containers.dashboardcontainer import applist_widget

from fedoracommunity.widgets import SubTabbedContainer
from links import updates_links

class UpdatesDashboardWidget(Widget):
    params = ['id', 'pending', 'testing', 'stable', 'username']
    template = 'mako:fedoracommunity.mokshaapps.updates.templates.dashboard_widget'

    def update_params(self, d):
        super(UpdatesDashboardWidget, self).update_params(d)
        bodhi = get_connector('bodhi')
        status = bodhi.get_dashboard_stats(username=d.username)
        d.pending = status['pending']
        d.testing = status['testing']
        d.stable = status['stable']

updates_dashboard_widget = UpdatesDashboardWidget('updates_dashboard')


class PendingUpdatesGrid(Grid, ContextAwareWidget):
    template='mako:fedoracommunity.mokshaapps.updates.templates.pending_table_widget'

class StableUpdatesGrid(Grid, ContextAwareWidget):
    template='mako:fedoracommunity.mokshaapps.updates.templates.stable_table_widget'

class TestingUpdatesGrid(Grid, ContextAwareWidget):
    template='mako:fedoracommunity.mokshaapps.updates.templates.testing_table_widget'

pending_updates_grid =  PendingUpdatesGrid('pending_updates_grid')
testing_updates_grid = TestingUpdatesGrid('testing_updates_grid')
stable_updates_grid = StableUpdatesGrid('stable_updates_grid')

unpushed_updates_app = MokshaApp('Unpushed Updates', 'fedoracommunity.updates/table',
                          params={
                              'rows_per_page': 10,
                              'filters': {
                                  'status':'pending',
                                  'profile': False,
                                  'username': None
                                  }
                              })
testing_updates_app = MokshaApp('Testing Updates', 'fedoracommunity.updates/table',
                          params={
                              'rows_per_page': 10,
                              'filters': {
                                  'status':'testing',
                                  'profile': False,
                                  'username': None
                                  }
                              })
stable_updates_app = MokshaApp('Stable Updates', 'fedoracommunity.updates/table',
                          params={
                              'rows_per_page': 10,
                              'filters': {
                                  'status':'stable',
                                  'profile': False,
                                  'username': None
                                  }
                              })

overview_updates_app = MokshaApp('Overview',
                                 'fedoracommunity.updates/overview',
                                 content_id='overview',
                                 params={'profile': False,
                                         'username': None})

dashboard_updates_app = MokshaApp('Updates Dashboard',
                                  'fedoracommunity.updates/dashboard',
                                  params={
                                      'username': '',
                                      })

class UpdatesOverviewContainer(DashboardContainer, ContextAwareWidget):
    javascript = [JSLink(link='/javascript/bodhi.js', modname=__name__)]
    layout = (Category('group-1-apps',
                       (dashboard_updates_app.clone(),
                        unpushed_updates_app.clone({'rows_per_page': 5,
                                                    'more_link_code': updates_links.UNPUSHED_UPDATES.code}),
                        testing_updates_app.clone({'rows_per_page': 5,
                                                    'more_link_code': updates_links.TESTING_UPDATES.code}))
                      ),
              Category('group-2-apps',
                       stable_updates_app.clone({'rows_per_page': 5,
                                                    'more_link_code': updates_links.STABLE_UPDATES.code})
                      )
             )

updates_overview_container = UpdatesOverviewContainer('updates_overview')

class UpdatesNavContainer(SubTabbedContainer):
    params = ['applist_widget']
    applist_widget = applist_widget

    template='mako:fedoracommunity.mokshaapps.updates.templates.updates_nav'
    sidebar_apps = (MokshaApp('Alerts', 'fedoracommunity.alerts'),)
    tabs = (Category('Packages I Own',
                     (overview_updates_app.clone({'profile': True},
                                                  content_id='my_overview_updates'),
                      unpushed_updates_app.clone({'filters': {'profile': True,
                                                  'group_updates': False}},
                                                 content_id='my_unpushed_updates'),
                      testing_updates_app.clone({'filters': {'profile': True,
                                                 'group_updates': False}},
                                                content_id='my_testing_updates'),
                      stable_updates_app.clone({'filters': {'profile': True,
                                                'group_updates': False}},
                                               content_id='my_stable_updates'),
                     ),
                     auth=not_anonymous()),
            Category('All Packages', (
                overview_updates_app,
                unpushed_updates_app.clone({
                    'filters': {'group_updates': False}
                    }),
                testing_updates_app.clone({
                   'filters': {'group_updates': False}
                    }),
                stable_updates_app.clone({
                    'filters': {'group_updates': False}
                    }),
                )
           )
        )

    def update_params(self, d):
        d['sidebar_apps'] = Category('sidebar-apps', self.sidebar_apps).process(d)

        super(UpdatesNavContainer, self).update_params(d)

updates_nav_container = UpdatesNavContainer('updates_nav')

class RootController(Controller):
    @expose('mako:moksha.templates.widget')
    def index(self, **kwds):
        options = {}

        tmpl_context.widget = updates_nav_container
        return {'options':options}

    @expose('mako:moksha.templates.widget')
    @validate(validators={'profile': validators.StringBool()})
    def overview(self, profile=False, username=None):
        options = {'profile': profile,
                   'username': username}
        tmpl_context.widget = updates_overview_container

        return {'options':options}

    @expose('mako:moksha.templates.widget')
    @validate(validators={'rows_per_page': validators.Int()})
    def table(self, rows_per_page=5, filters=None, more_link_code=None):
        ''' table handler

        This handler displays the main table by itself
        '''
        if not filters:
            filters = {}

        if isinstance(filters, basestring):
            decoded_filters = json.loads(filters)
        else:
            decoded_filters = filters

        more_link = None
        if more_link_code:
            more_link = updates_links.get_data(more_link_code)

            if asbool(decoded_filters.get('profile')) == True:
                s = more_link.split('/')
                last = s[-1]
                last = 'my_' + last
                s[-1] = last

                more_link = '/'.join(s)

        status = decoded_filters.get('status','').lower()
        if status == 'stable':
            tmpl_context.widget = stable_updates_grid
        elif status == 'testing':
            tmpl_context.widget = testing_updates_grid
        elif status == 'pending':
            tmpl_context.widget = pending_updates_grid
        else:
            tmpl_context.widget = stable_updates_grid

        options = dict(filters=filters, rows_per_page=rows_per_page,
                       resource='bodhi', resource_path='query_updates',
                       more_link=more_link)

        return dict(options=options)

    @expose('mako:moksha.templates.widget')
    def dashboard(self, *args, **kw):
        options = {}
        tmpl_context.widget = updates_dashboard_widget
        if request.identity:
            options['username'] = request.identity['person']['username']
        return dict(options=options)
