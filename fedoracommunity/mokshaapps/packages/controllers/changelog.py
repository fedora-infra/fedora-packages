from moksha.lib.base import Controller
from moksha.lib.helpers import Category, MokshaApp, Not, not_anonymous, Widget
from moksha.api.widgets.containers import DashboardContainer
from moksha.api.widgets import ContextAwareWidget, Grid

from tg import expose, tmpl_context, require, request

from helpers import PackagesDashboardContainer

class ChangelogGrid(ContextAwareWidget, Grid):
    template='mako:fedoracommunity.mokshaapps.packages.templates.changelog_table_widget'

    def update_params(self, d):
        d['resource'] = 'koji',
        d['resource_path'] = 'query_changelogs'
        super(ChangelogGrid, self).update_params(d)

changelog_grid = ChangelogGrid('changelog_table')

class ChangelogDashboard(PackagesDashboardContainer):
    template = 'mako:fedoracommunity.mokshaapps.packages.templates.single_col_dashboard'
    layout = [Category('content-col-apps',[
                          Widget('Latest Build Changelogs',
                                 changelog_grid,
                                 params={'filters':{'package': ''}})
                       ])]

changelog_dashboard = ChangelogDashboard('changelog_dashboard')

class ChangelogController(Controller):
    @expose('mako:moksha.templates.widget')
    def index(self, package):
        tmpl_context.widget = changelog_dashboard
        return {'options':{'package': package}}
