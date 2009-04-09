from tg import expose, tmpl_context

from moksha.lib.base import Controller
from moksha.lib.helpers import Category
from moksha.api.widgets.containers import DashboardContainer
from moksha.api.widgets import ContextAwareWidget

class VersionsDashboard(DashboardContainer, ContextAwareWidget):
    template = 'mako:fedoracommunity.mokshaapps.packages.templates.single_col_dashboard'
    layout = [Category('content-col-apps',[])]

versions_dashboard = VersionsDashboard

class VersionsController(Controller):
    @expose('mako:moksha.templates.widget')
    def index(self, package):
        tmpl_context.widget = versions_dashboard
        return {'package': package}
