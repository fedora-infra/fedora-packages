from moksha.lib.base import Controller
from moksha.lib.helpers import Category, MokshaApp, Not, not_anonymous, MokshaWidget, Widget
from moksha.api.widgets.containers import DashboardContainer
from moksha.api.widgets import ContextAwareWidget
from tw.api import Widget as twWidget

from tg import expose, tmpl_context, require, request

from bugs import BugsController
from builds import BuildsController
from changelog import ChangelogController
from downloads import DownloadsController
from acls import AclsController
from updates import UpdatesController
from versions import VersionsController

from helpers import PackagesDashboardContainer

class PkgDetails(twWidget):
    template = 'mako:fedoracommunity.mokshaapps.packages.templates.pkgdetails'

pkg_details_widget = PkgDetails('details')

class PkgLinks(twWidget):
    template = 'mako:fedoracommunity.mokshaapps.packages.templates.pkglinks'

pkg_links_widget = PkgLinks('details')

class OverviewDashboard(PackagesDashboardContainer):
    template = 'mako:fedoracommunity.mokshaapps.packages.templates.single_col_dashboard'
    layout = [Category('content-col-apps',(Widget('Description', pkg_details_widget,
                                                  params={'pkg_description': '', 'owner': ''}),
                                           MokshaApp('Active Releases',
                                                     'fedoracommunity.updates/table',
                                                     params={'filters':{'package':''}}),
                                           Widget('Package Links', pkg_links_widget,
                                                  params={'package':''}),
                                           MokshaApp('Latest Changelog Entries',
                                                     'fedoracommunity.packages/package/changelog/table',
                                                     params={'package':''})

                                           )
                      )
              ]

overview_dashboard = OverviewDashboard('overview_dashboard')

class OverviewController(Controller):
    bugs = BugsController()
    builds = BuildsController()
    changelog = ChangelogController()
    downloads = DownloadsController()
    acls = AclsController()
    updates = UpdatesController()
    verisons = VersionsController()

    @expose('mako:moksha.templates.widget')
    def index(self, **kwds):
        tmpl_context.widget = overview_dashboard
        return {'options': kwds}

    @expose('mako:moksha.templates.widget')
    def overview(self, package):
        tmpl_context.widget = overview_dashboard
        return dict(options={'package':package})
