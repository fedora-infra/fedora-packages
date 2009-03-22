from tg import expose, tmpl_context, validate, request
from tw.api import JSLink
from tw.jquery import jQuery, jquery_js, js_callback
from formencode import validators

from moksha.lib.base import Controller
from moksha.lib.helpers import Category, MokshaApp, Not, not_anonymous, MokshaWidget, Widget, check_predicates
from moksha.api.widgets import ContextAwareWidget, Grid, Selectable
from moksha.api.widgets.containers import DashboardContainer

class PendingUpdatesGrid(Grid, ContextAwareWidget):
    template='mako:fedoracommunity.mokshaapps.updates.templates.pending_table_widget'

class StableUpdatesGrid(Grid, ContextAwareWidget):
    template='mako:fedoracommunity.mokshaapps.updates.templates.stable_table_widget'

class TestingUpdatesGrid(Grid, ContextAwareWidget):
    template='mako:fedoracommunity.mokshaapps.updates.templates.testing_table_widget'

pending_updates_grid =  PendingUpdatesGrid('pending_updates_grid')
testing_updates_grid = TestingUpdatesGrid('testing_updates_grid')
stable_updates_grid = StableUpdatesGrid('stable_updates_grid')

class UpdatesFilter(Selectable):
    updates_filter_js = JSLink(modname='fedoracommunity.mokshaapps.updates',
                               filename='javascript/updatesfilter.js')
    javascript = [updates_filter_js] + Selectable.javascript

    def update_params(self, d):
        super(UpdatesFilter, self).update_params(d)
        categories = []

        if check_predicates(not_anonymous()):
            cat = {
                  }

            categories.append(cat)


        cat = {'label': 'All Packages',
               'items': [{'label': 'Unpushed Updates',
                          'link':'javascript:void(0);',
                          'data':{
                                  'rows_per_page': 10,
                                  'filters': {'status':'pending'}
                                 }
                         },
                         {'label': 'Testing Updates',
                          'link':'javascript:void(0);',
                          'data': {
                                   'rows_per_page': 10,
                                   'filters':{'status':'testing'}
                                  }
                         },
                         {'label': 'Stable Updates',
                          'link':'javascript:void(0);',
                          'data': {
                                   'rows_per_page': 10,
                                   'filters':{'status':'stable'}
                                  }
                         }]
                }

        categories.append(cat)
        d.update({'categories': categories})

        self.add_call('$("#%s").bind("selected", _updates_filter_selected)' % d.content_id)

updates_filter = UpdatesFilter('updates_filter')
updates_grid = UpdatesGrid('updates_table')

class UpdatesContainer(DashboardContainer, ContextAwareWidget):
    unpushed_updates_app = MokshaApp('Unpushed Updates', 'fedoracommunity.updates/table',
                                       css_class='main_table',
                                       params={'rows_per_page': 5,
                                               'filters':{'status':'pending'}})
    testing_updates_app = MokshaApp('Testing Updates', 'fedoracommunity.updates/table',
                                       css_class='secondary_table',
                                       params={'rows_per_page': 5,
                                               'filters':{'status':'testing'}})
    stable_updates_app = MokshaApp('Stable Updates', 'fedoracommunity.updates/table',
                                       css_class='secondary_table',
                                       params={'rows_per_page': 5,
                                               'filters':{'status':'stable'}})

    layout = [Category('right-content-column',
                        (Widget('Filters', updates_filter
                                 ),
                        MokshaApp('Alerts', 'fedoracommunity.alerts'))),
              Category('left-content-column',
                        (unpushed_updates_app,
                        testing_updates_app,
                        stable_updates_app))]

    def update_params(self, d):
        super(UpdatesContainer, self).update_params(d)

updates_container = UpdatesContainer('updates_container')

class RootController(Controller):

    # do something for index, this should be the container stuff
    @expose('mako:moksha.templates.widget')
    def index(self, **kwds):
        options = {}

        tmpl_context.widget = updates_container
        return {'options':options}

    @expose('mako:moksha.templates.widget')
    @validate(validators={'rows_per_page': validators.Int()})
    def table(self, uid="", rows_per_page=5, filters=None):
        ''' table handler

        This handler displays the main table by itself
        '''
        if not filters:
            filters = {}
        if 'stable' in filters:
            tmpl_context.widget = stable_updates_grid
        elif 'testing' in filters:
            tmpl_context.widget = testing_updates_grid
        elif 'pending' in filters:
            tmpl_context.widget = pending_updates_grid
        else:
            tmpl_context.widget = stable_updates_grid

        options = dict(filters=filters, uid=uid, rows_per_page=rows_per_page,
                       resource='bodhi', resource_path='query_updates')

        return dict(options=options)
