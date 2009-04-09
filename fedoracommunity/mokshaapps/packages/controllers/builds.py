from tg import expose, tmpl_context

from moksha.lib.base import Controller
from moksha.lib.helpers import Category, MokshaApp

from helpers import PackagesDashboardContainer

class BuildsDashboard(PackagesDashboardContainer):
    layout = [Category('content-col-apps',
                       MokshaApp('Builds', 'fedoracommunity.builds/table',
                                 params={'filters':{'package':''}}))]

builds_dashboard = BuildsDashboard('builds_dashboard')

class BuildsController(Controller):
    @expose('mako:moksha.templates.widget')
    def index(self, package):
        tmpl_context.widget = builds_dashboard
        return {'options':{'package': package}}
