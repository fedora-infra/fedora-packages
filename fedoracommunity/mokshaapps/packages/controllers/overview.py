from moksha.lib.base import Controller
from moksha.lib.helpers import Category, MokshaApp, Not, not_anonymous, MokshaWidget
from moksha.api.widgets.containers import DashboardContainer
from moksha.api.widgets import ContextAwareWidget

from tg import expose, tmpl_context, require, request

from bugs import BugsController
from builds import BuildsController
from changelog import ChangelogController
from downloads import DownloadsController
from maintainers import MaintainersController
from owners import OwnersController
from updates import UpdatesController
from versions import VersionsController
from watchers import WatchersController

class OverviewDashboard(DashboardContainer, ContextAwareWidget):
    template = 'mako:fedoracommunity.mokshaapps.packages.templates.single_col_dashboard'
    layout = [Category('content-col-apps',[])]

overview_dashboard = OverviewDashboard

class OverviewController(Controller):
    bugs = BugsController()
    builds = BuildsController()
    changelog = ChangelogController()
    downloads = DownloadsController()
    maintainers = MaintainersController()
    owners = OwnersController()
    updates = UpdatesController()
    verisons = VersionsController()
    watchers = WatchersController()

    @expose('mako:moksha.templates.widget')
    def index(self, package):
        tmpl_context.widget = overview_dashboard
        return dict(package=package, options={})

    @expose('mako:moksha.templates.widget')
    def overview(self, package):
        tmpl_context.widget = overview_dashboard
        return dict(package=package, options={})
