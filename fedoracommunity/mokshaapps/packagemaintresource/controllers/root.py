from moksha.lib.base import BaseController
from tg import expose, tmpl_context
from fedoracommunity.widgets import SubTabbedContainer

class TabbedNav(SubTabbedContainer):
    tabs= '(MokshaApp("Overview", ""), MokshaApp("Builds", ""))'
    
class RootController(BaseController):
    def __init__(self):
        self.widget = TabbedNav('packagemaintnav')

    @expose('mako:fedoracommunity.mokshaapps.packagemaintresource.templates.index')
    def index(self):
        tmpl_context.widget = self.widget
        return {}
