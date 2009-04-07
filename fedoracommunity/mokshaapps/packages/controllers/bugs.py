from tw.api import Widget as TWWidget
from pylons import cache
from moksha.lib.base import Controller
from moksha.lib.helpers import Category, MokshaApp, Not, not_anonymous, MokshaWidget
from moksha.lib.helpers import Widget
from moksha.api.widgets.containers import DashboardContainer
from moksha.api.widgets import ContextAwareWidget, Grid
from moksha.api.connectors import get_connector
from helpers import PackagesDashboardContainer

from tg import expose, tmpl_context, require, request

class BugStatsWidget(TWWidget):
    template='mako:fedoracommunity.mokshaapps.packages.templates.bugs_stats_widget'
    params = ['id', 'product', 'component', 'version', 'num_closed',
              'num_open', 'num_new']
    product = 'Fedora'
    version = 'rawhide'
    component = None
    num_closed = num_open = num_new = '-'

bug_stats_widget = BugStatsWidget('bug_stats')


class BugsGrid(Grid):
    template='mako:fedoracommunity.mokshaapps.packages.templates.bugs_table_widget'

    def update_params(self, d):
        d['resource'] = 'bugzilla'
        d['resource_path'] = 'query_bugs'
        super(BugsGrid, self).update_params(d)

bugs_grid = BugsGrid('bugs_grid')


class BugsDashboard(PackagesDashboardContainer):
    layout = [Category('content-col-apps',[
                         Widget('Dashboard', bug_stats_widget,
                                params={'filters':{'package': ''}}),
                         Widget('Recently Filed Bugs',
                                bugs_grid,
                                params={'filters':{'package': ''}}),
                         ])]

bugs_dashboard = BugsDashboard('bugs_dashboard')


class BugsController(Controller):

    @expose('mako:moksha.templates.widget')
    def index(self, package):
        tmpl_context.widget = bugs_dashboard
        return {'options': {'package': package}}
