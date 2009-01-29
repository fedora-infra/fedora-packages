from moksha.lib.base import BaseController
from moksha.lib.helpers import Category, MokshaApp, Not, not_anonymous
from moksha.api.widgets.containers import DashboardContainer
from moksha.api.widgets import ContextAwareWidget
from tg import expose, tmpl_context

class OverviewContainer(DashboardContainer, ContextAwareWidget):
    template = 'mako:fedoracommunity.mokshaapps.overviewresource.templates.overviewcontainer'
    layout = [Category('left-content-column',
                       [MokshaApp('Latest Rawhide Builds', 'fedoracommunity.builds/table'),
                        MokshaApp('Latest Stable Updates','fedoracommunity.updates/table', 
                                  {"filters":'{"status":"stable"}', "uid":"stable"}),
                        MokshaApp('Latest Testing Updates','fedoracommunity.updates/table', 
                                  {"filters":'{"status":"testing"}', "uid":"testing"})
                        ]),
              Category('right-content-column',
                       [MokshaApp(None, 'login', auth=Not(not_anonymous()))])]

overview_container = OverviewContainer('overview')

class RootController(BaseController):

    @expose('mako:fedoracommunity.mokshaapps.overviewresource.templates.index')
    def index(self):
        tmpl_context.widget = overview_container
        
        return dict()
