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
            categories.append({
                'label': 'Packages I Own',
                'items': [
                    {
                        'label': 'Unpushed Updates',
                        'link':'javascript:void(0);',
                        'data': {
                            'rows_per_page': 10,
                            'filters': {
                                'status': 'pending',
                                'profile': True,
                            },
                        }
                    },
                    {
                        'label': 'Testing Updates',
                        'link':'javascript:void(0);',
                        'data': {
                            'rows_per_page': 10,
                            'filters': {
                                'status': 'testing',
                                'profile': True,
                            },
                        }
                    },
                    {
                        'label': 'Stable Updates',
                        'link':'javascript:void(0);',
                        'data': {
                            'rows_per_page': 10,
                            'filters': {
                                'status':'stable',
                                'profile': True,
                            },
                        }
                    }
                ]
            })

        categories.append({
            'label': 'All Packages',
            'items': [
                {
                    'label': 'Unpushed Updates',
                    'link':'javascript:void(0);',
                    'data': {
                        'rows_per_page': 10,
                        'filters': {'status': 'pending'},
                     }
                },
                {
                    'label': 'Testing Updates',
                    'link':'javascript:void(0);',
                    'data': {
                        'rows_per_page': 10,
                        'filters':{'status': 'testing'},
                    }
                },
                {
                    'label': 'Stable Updates',
                    'link':'javascript:void(0);',
                    'data': {
                        'rows_per_page': 10,
                        'filters':{'status': 'stable'},
                    }
                 }
            ]
        })

        d.update({'categories': categories})

        self.add_call('$("#%s").bind("selected", _updates_filter_selected)' %
                      d.content_id)

updates_filter = UpdatesFilter('updates_filter')
#updates_grid = UpdatesGrid('updates_table')

class AnonymousUpdatesContainer(DashboardContainer, ContextAwareWidget):
    layout = [
            Category('right-content-column', (
                Widget('Filters', updates_filter),
                MokshaApp('Alerts', 'fedoracommunity.alerts')
                )),
            Category('left-content-column', (
                MokshaApp('Unpushed Updates', 'fedoracommunity.updates/table',
                          css_class='main_table', params={'rows_per_page': 5,
                              'filters': {'status':'pending'}}),
                MokshaApp('Testing Updates', 'fedoracommunity.updates/table',
                          css_class='secondary_table', params={
                              'rows_per_page': 5,
                              'filters': {'status':'testing'}}),
                MokshaApp('Stable Updates', 'fedoracommunity.updates/table',
                          css_class='secondary_table', params={
                              'rows_per_page': 5,
                              'filters': {'status':'stable'}}),
                ))
    ]

class UpdatesContainer(DashboardContainer, ContextAwareWidget):
    layout = [
            Category('right-content-column', (
                Widget('Filters', updates_filter),
                MokshaApp('Alerts', 'fedoracommunity.alerts')
                )),
            Category('left-content-column', (
                MokshaApp('Unpushed Updates', 'fedoracommunity.updates/table',
                          css_class='main_table', params={
                              'rows_per_page': 5,
                              'filters': {
                                  'status':'pending',
                                  'profile': True
                                  }
                              }),
                MokshaApp('Testing Updates', 'fedoracommunity.updates/table',
                          css_class='secondary_table', params={
                              'rows_per_page': 5,
                              'filters': {
                                  'status':'testing',
                                  'profile': True
                                  }
                              }),
                MokshaApp('Stable Updates', 'fedoracommunity.updates/table',
                          css_class='secondary_table', params={
                              'rows_per_page': 5,
                              'filters': {
                                  'status':'stable',
                                  'profile': True
                                  }
                              }),
                ))
    ]


anonymous_updates_container = AnonymousUpdatesContainer('updates_container')
updates_container = UpdatesContainer('updates_container')

class RootController(Controller):

    @expose('mako:moksha.templates.widget')
    def index(self, **kwds):
        options = {}
        if request.identity:
            tmpl_context.widget = updates_container
        else:
            tmpl_context.widget = anonymous_updates_container
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
