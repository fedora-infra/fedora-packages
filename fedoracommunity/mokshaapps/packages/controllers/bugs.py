from tw.api import Widget as TWWidget
from tg import expose, tmpl_context

from moksha.lib.base import Controller
from moksha.lib.helpers import Category
from moksha.lib.helpers import Widget
from moksha.api.widgets import Grid

from helpers import PackagesDashboardContainer

class BugStatsWidget(TWWidget):
    template='mako:fedoracommunity.mokshaapps.packages.templates.bugs_stats_widget'
    params = ['id', 'product', 'package', 'version', 'num_closed',
              'num_open', 'num_new', 'num_new_this_week', 'num_closed_this_week']
    product = 'Fedora'
    version = 'rawhide'
    package = None
    num_closed = num_open = num_new = '-'
    num_new_this_week = num_closed_this_week = ''

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
                         Widget('Bugs Dashboard', bug_stats_widget,
                                params={'package': '', 'filters':{'package': ''}}),
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
