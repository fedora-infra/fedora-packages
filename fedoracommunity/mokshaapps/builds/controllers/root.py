from tg import expose, tmpl_context
from koji import BUILD_STATES

from paste.deploy.converters import asbool

from moksha.lib.base import Controller
from moksha.lib.helpers import Category, MokshaApp, not_anonymous
from moksha.api.widgets import ContextAwareWidget, Grid
from moksha.api.widgets.containers import DashboardContainer
from moksha.api.widgets.containers.dashboardcontainer import applist_widget

from fedoracommunity.widgets import SubTabbedContainer
from links import builds_links

import simplejson as json

class BuildsGrid(Grid, ContextAwareWidget):
    template='mako:fedoracommunity.mokshaapps.builds.templates.table_widget'

class BuildsPackagesGrid(Grid, ContextAwareWidget):
    template='mako:fedoracommunity.mokshaapps.builds.templates.packages_table_widget'


in_progress_builds_app = MokshaApp('In-progress Builds', 'fedoracommunity.builds/table',
                                       css_class='main_table',
                                       content_id='inprogress',
                                       params={'rows_per_page': 10,
                                               'filters':{'state':BUILD_STATES['BUILDING'],
                                                          'profile': False,
                                                          'username': None
                                                         }
                                              })

failed_builds_app = MokshaApp('Failed Builds', 'fedoracommunity.builds/table',
                                       css_class='secondary_table',
                                       content_id='failed',
                                       params={'rows_per_page': 10,
                                               'filters':{'state':BUILD_STATES['FAILED'],
                                                          'profile': False,
                                                          'username': None
                                                         }
                                              })

successful_builds_app = MokshaApp('Successful Builds', 'fedoracommunity.builds/table',
                                       css_class='secondary_table',
                                       content_id='successful',
                                       params={'rows_per_page': 10,
                                               'filters':{'state':BUILD_STATES['COMPLETE'],
                                                          'profile': False,
                                                          'username': None
                                                         }
                                              })

overview_builds_app = MokshaApp('Overview',
                                 'fedoracommunity.builds/overview',
                                 content_id='builds_overview',
                                 params={'profile': False,
                                         'username': None})

class BuildsNavContainer(SubTabbedContainer):
    params = ['applist_widget']
    applist_widget = applist_widget
    template='mako:fedoracommunity.mokshaapps.builds.templates.builds_nav'
    sidebar_apps = (MokshaApp('Alerts', 'fedoracommunity.alerts', css_class='app panel'),)
    tabs = (Category('Packages I Own',
                     (overview_builds_app.clone({'profile': True},
                                                content_id='my_builds_overview'),
                      in_progress_builds_app.clone({'filters': {'profile': True}},
                                                   content_id='my_inprogress'),
                      failed_builds_app.clone({'filters': {'profile': True}},
                                                   content_id='my_failed'),
                      successful_builds_app.clone({'filters': {'profile': True}},
                                                   content_id='my_successful'),
                     ),
                     auth=not_anonymous()),
            Category('All Packages',
                     (overview_builds_app,
                      in_progress_builds_app,
                      failed_builds_app,
                      successful_builds_app)
                    )
           )

    def update_params(self, d):
        d['sidebar_apps'] = Category('sidebar-apps', self.sidebar_apps).process(d)

        super(BuildsNavContainer, self).update_params(d)

builds_nav_container = BuildsNavContainer('builds_nav')

builds_grid = BuildsGrid('builds_table')
builds_packages_grid = BuildsPackagesGrid('builds_packages_table')

class BuildsOverviewContainer(DashboardContainer, ContextAwareWidget):

    layout = [Category('group-1-apps',
                        (in_progress_builds_app.clone({'rows_per_page': 5,
                                                       'more_link_code': builds_links.IN_PROGRESS.code}),
                        failed_builds_app.clone({'rows_per_page': 5,
                                                       'more_link_code': builds_links.FAILED.code}))
                      ),
              Category('group-2-apps',
                       successful_builds_app.clone({'rows_per_page': 5,
                                                       'more_link_code': builds_links.SUCCESSFUL.code})
                      )
             ]

builds_overview_container = BuildsOverviewContainer('builds_overview')

class RootController(Controller):

    @expose('mako:moksha.templates.widget')
    def index(self, **kwds):
        options = {}

        tmpl_context.widget = builds_nav_container
        return {'options':options}

    @expose('mako:moksha.templates.widget')
    def overview(self, profile=False, username=None):
        options = {'profile': profile,
                   'username': username}

        tmpl_context.widget = builds_overview_container
        return {'options':options}

    @expose('mako:moksha.templates.widget')
    def name(self, pkg_name, **kwds):

        kwds.update({'p': pkg_name})
        return self.index(**kwds)

    @expose('mako:fedoracommunity.mokshaapps.builds.templates.packages_table')
    def packages_table(self, uid="", rows_per_page=5, filters=None, more_link_code=None):
        if isinstance(rows_per_page, basestring):
            rows_per_page = int(rows_per_page)

        if filters == None:
            filters = {}

        more_link = None
        if more_link_code:
            more_link = builds_links.get_data(more_link_code)

        tmpl_context.widget = builds_packages_grid
        return {'filters': filters, 'rows_per_page':rows_per_page,
                'more_link': more_link}

    @expose('mako:fedoracommunity.mokshaapps.builds.templates.table')
    def table(self, uid="", rows_per_page=5, filters=None, more_link_code=None):
        ''' table handler

        This handler displays the main table by itself
        '''

        if isinstance(rows_per_page, basestring):
            rows_per_page = int(rows_per_page)

        if filters == None:
            filters = {}

        more_link = None
        if more_link_code:
            more_link = builds_links.get_data(more_link_code)
            if isinstance(filters, basestring):
                decoded_filters = json.loads(filters)
            else:
                decoded_filters = filters

            if asbool(decoded_filters.get('profile')) == True:
                s = more_link.split('/')
                last = s[-1]
                last = 'my_' + last
                s[-1] = last

                more_link = '/'.join(s)

        tmpl_context.widget = builds_grid
        return {'filters': filters, 'uid':uid, 'rows_per_page':rows_per_page,
                'more_link': more_link}
