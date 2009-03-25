from moksha.lib.base import Controller
from moksha.lib.helpers import Category, MokshaApp, Not, not_anonymous, MokshaWidget
from moksha.api.widgets.containers import DashboardContainer
from moksha.api.widgets import ContextAwareWidget

from tg import expose, tmpl_context, require, request

class UpdatesDashboard(DashboardContainer, ContextAwareWidget):
    template = 'mako:fedoracommunity.mokshaapps.packages.templates.single_col_dashboard'
    layout = [Category('content-col-apps',[])]

updates_dashboard = UpdatesDashboard

class UpdatesController(Controller):
    @expose('mako:moksha.templates.widget')
    def index(self, package):
        tmpl_context.widget = updates_dashboard
        return {'package': package}
