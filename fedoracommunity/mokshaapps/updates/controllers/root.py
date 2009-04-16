from tg import expose, tmpl_context, validate
from tw.api import JSLink
from formencode import validators
from paste.deploy.converters import asbool

import simplejson as json

from moksha.lib.base import Controller
from moksha.lib.helpers import Category, MokshaApp, not_anonymous
from moksha.api.widgets import ContextAwareWidget, Grid
from moksha.api.widgets.containers import DashboardContainer
from moksha.api.widgets.containers.dashboardcontainer import applist_widget

from fedoracommunity.widgets import SubTabbedContainer

from links import updates_links

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
                          css_class='main_table', params={
                              'rows_per_page': 10,
                              'filters': {
                                  'status':'pending',
                                  'profile': False
                                  }
                              })
testing_updates_app = MokshaApp('Testing Updates', 'fedoracommunity.updates/table',
                          css_class='secondary_table', params={
                              'rows_per_page': 10,
                              'filters': {
                                  'status':'testing',
                                  'profile': False
                                  }
                              })
stable_updates_app = MokshaApp('Stable Updates', 'fedoracommunity.updates/table',
                          css_class='secondary_table', params={
                              'rows_per_page': 10,
                              'filters': {
                                  'status':'stable',
                                  'profile': False
                                  }
                              })

overview_updates_app = MokshaApp('Overview',
                                 'fedoracommunity.updates/overview',
                                 content_id='overview',
                                 params={'profile': False})

class UpdatesOverviewContainer(DashboardContainer, ContextAwareWidget):
    javascript = [JSLink(link='/javascript/bodhi.js', modname=__name__)]
    layout = (Category('group-1-apps',
                       (unpushed_updates_app.clone({'rows_per_page': 5,
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
                      unpushed_updates_app.clone({'filters': {'profile': True}},
                                                   content_id='my_unpushed_updates'),
                      testing_updates_app.clone({'filters': {'profile': True}},
                                                   content_id='my_testing_updates'),
                      stable_updates_app.clone({'filters': {'profile': True}},
                                                   content_id='my_stable_updates'),
                     ),
                     auth=not_anonymous()),
            Category('All Packages',
                     (overview_updates_app,
                      unpushed_updates_app,
                      testing_updates_app,
                      stable_updates_app)
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
    def overview(self, profile=False):
        options = {'profile': profile}
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

        if decoded_filters.get('status').lower() == 'stable':
            tmpl_context.widget = stable_updates_grid
        elif decoded_filters.get('status').lower() == 'testing':
            tmpl_context.widget = testing_updates_grid
        elif decoded_filters.get('status').lower() == 'pending':
            tmpl_context.widget = pending_updates_grid
        else:
            tmpl_context.widget = stable_updates_grid

        options = dict(filters=filters, rows_per_page=rows_per_page,
                       resource='bodhi', resource_path='query_updates',
                       more_link=more_link)

        return dict(options=options)
