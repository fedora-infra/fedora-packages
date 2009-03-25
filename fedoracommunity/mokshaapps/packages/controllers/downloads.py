from moksha.lib.base import Controller
from moksha.lib.helpers import Category, MokshaApp, Not, not_anonymous, MokshaWidget
from moksha.api.widgets.containers import DashboardContainer
from moksha.api.widgets import ContextAwareWidget

from tg import expose, tmpl_context, require, request

class DownloadsDashboard(DashboardContainer, ContextAwareWidget):
    template = 'mako:fedoracommunity.mokshaapps.packages.templates.single_col_dashboard'
    layout = [Category('content-col-apps',[])]

class SourceDashboard(DashboardContainer, ContextAwareWidget):
    template = 'mako:fedoracommunity.mokshaapps.packages.templates.single_col_dashboard'
    layout = [Category('content-col-apps',[])]

downloads_dashboard = DownloadsDashboard
source_dashboard = SourceDashboard

class DownloadsController(Controller):
    @expose('mako:moksha.templates.widget')
    def index(self, package):
        tmpl_context.widget = download_dashboard
        return {'package': package}

    def source(self, package):
        tmpl_context.widget = source_dashboard
        return {'package': package}
