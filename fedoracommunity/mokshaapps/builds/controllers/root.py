from moksha.lib.base import Controller
from moksha.lib.helpers import Category, MokshaApp, Not, not_anonymous, MokshaWidget, Widget, check_predicates
from moksha.api.widgets import ContextAwareWidget, Grid, Selectable
from moksha.api.widgets.containers import DashboardContainer
from koji import BUILD_STATES
from tg import expose, tmpl_context, request

from tw.api import JSLink
from tw.jquery import jQuery, jquery_js, js_callback

from links import builds_links

class BuildsGrid(Grid, ContextAwareWidget):
    template='mako:fedoracommunity.mokshaapps.builds.templates.table_widget'

class BuildsFilter(Selectable):
    builds_filter_js = JSLink(modname='fedoracommunity.mokshaapps.builds',
                              filename='javascript/buildsfilter.js')
    javascript = [builds_filter_js] + Selectable.javascript

    def update_params(self, d):
        super(BuildsFilter, self).update_params(d)
        categories = []

        if check_predicates(not_anonymous()):
            cat = {'label': 'Packages I Own',
                   'items': [{'label': 'In Progress Builds',
                              'link':'javascript:void(0);',
                              'data':{
                                      'rows_per_page': 10,
                                      'filters': {'state':BUILD_STATES['BUILDING'],
                                                  'profile': True
                                                 }
                                     }
                              },
                              {'label': 'Failed Builds',
                              'link':'javascript:void(0);',
                              'data':{
                                      'rows_per_page': 10,
                                      'filters': {'state':BUILD_STATES['FAILED'],
                                                  'profile': True
                                                  }
                                     }
                              },
                              {'label': 'Successful Builds',
                              'link':'javascript:void(0);',
                              'data':{
                                      'rows_per_page': 10,
                                      'filters': {'state':BUILD_STATES['COMPLETE'],
                                                  'profile': True
                                                  }
                                     }
                              }
                              ]
                  }

            categories.append(cat)


        cat = {'label': 'All Packages',
               'items': [{'label': 'In Progress Builds',
                          'link':'javascript:void(0);',
                          'data':{
                                  'rows_per_page': 10,
                                  'filters': {'state':BUILD_STATES['BUILDING']}
                                 }
                         },
                         {'label': 'Failed Builds',
                          'link':'javascript:void(0);',
                          'data': {
                                   'rows_per_page': 10,
                                   'filters':{'state':BUILD_STATES['FAILED']}
                                  }
                         },
                         {'label': 'Successful Builds',
                          'link':'javascript:void(0);',
                          'data': {
                                   'rows_per_page': 10,
                                   'filters':{'state':BUILD_STATES['COMPLETE']}
                                  }
                         }]
                }

        categories.append(cat)
        d.update({'categories': categories})

        self.add_call('$("#%s").bind("selected", _builds_filter_selected)' % d.content_id)

builds_filter = BuildsFilter('builds_filter')

class BuildsContainer(DashboardContainer, ContextAwareWidget):
    in_progress_builds_app = MokshaApp('In-progress Builds', 'fedoracommunity.builds/table',
                                       css_class='main_table',
                                       params={'rows_per_page': 5,
                                               'filters':{'state':BUILD_STATES['BUILDING']}})
    failed_builds_app = MokshaApp('Failed Builds', 'fedoracommunity.builds/table',
                                       css_class='secondary_table',
                                       params={'rows_per_page': 5,
                                               'filters':{'state':BUILD_STATES['FAILED']}})
    successful_builds_app = MokshaApp('Successful Builds', 'fedoracommunity.builds/table',
                                       css_class='secondary_table',
                                       params={'rows_per_page': 5,
                                               'filters':{'state':BUILD_STATES['COMPLETE']}})

    layout = [Category('right-content-column',
                        (Widget('Filters', builds_filter,
                                  params={'in_progress': in_progress_builds_app,
                                          'failed': failed_builds_app,
                                          'successful': successful_builds_app
                                         }
                                 ),
                        MokshaApp('Alerts', 'fedoracommunity.alerts'))),
              Category('left-content-column',
                        (in_progress_builds_app,
                        failed_builds_app,
                        successful_builds_app))]

    def update_params(self, d):
        super(BuildsContainer, self).update_params(d)

builds_container = BuildsContainer('builds')
builds_grid = BuildsGrid('builds_table')

class RootController(Controller):

    # do something for index, this should be the container stuff
    @expose('mako:moksha.templates.widget')
    def index(self, **kwds):
        options = {}

        tmpl_context.widget = builds_container
        return {'options':options}

    @expose('mako:moksha.templates.widget')
    def name(self, pkg_name, **kwds):

        kwds.update({'p': pkg_name})
        return self.index(**kwds)

    @expose('mako:fedoracommunity.mokshaapps.builds.templates.table')
    def table(self, uid="", rows_per_page=5, filters={}, more_link_code=None):
        ''' table handler

        This handler displays the main table by itself
        '''

        if isinstance(rows_per_page, basestring):
            rows_per_page = int(rows_per_page)

        more_link = None
        if more_link_code:
            more_link = builds_links.get_data(more_link_code)

        tmpl_context.widget = builds_grid
        return {'filters': filters, 'uid':uid, 'rows_per_page':rows_per_page,
                'more_link': more_link}
