from moksha.lib.base import BaseController
from moksha.api.widgets.containers import DashboardContainer
from tg import expose, tmpl_context

class OverviewContainer(DashboardContainer):
    template = 'mako:fedoracommunity.mokshaapps.overviewresource.templates.overviewcontainer'
    layout = "[Category('left-content-column',[MokshaApp('Hello World', 'helloworld')])," 
    layout += "Category('right-content-column',[MokshaApp(None, 'login' , auth=[Not(not_anonymous())])])]"

overview_container = OverviewContainer('overview')

class RootController(BaseController):

    @expose('mako:fedoracommunity.mokshaapps.overviewresource.templates.index')
    def index(self):
        tmpl_context.widget = overview_container
        
        return dict()
