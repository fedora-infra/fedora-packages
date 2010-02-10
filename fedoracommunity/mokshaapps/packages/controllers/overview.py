# This file is part of Fedora Community.
# Copyright (C) 2008-2010  Red Hat, Inc.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from tw.api import Widget as twWidget
from tg import expose, tmpl_context

from moksha.api.connectors import get_connector
from moksha.api.widgets import ContextAwareWidget
from moksha.lib.base import Controller
from moksha.lib.helpers import Category, MokshaApp, Widget

from bugs import BugsController
from builds import BuildsController
from changelog import ChangelogController
from downloads import DownloadsController
from acls import AclsController
from updates import UpdatesController
from versions import VersionsController
from helpers import PackagesDashboardContainer
from links import changelog_links

class PkgDetails(ContextAwareWidget):
    template = 'mako:fedoracommunity.mokshaapps.packages.templates.pkgdetails'

pkg_details_widget = PkgDetails('details')

class PkgLinks(ContextAwareWidget):
    template = 'mako:fedoracommunity.mokshaapps.packages.templates.pkglinks'

pkg_links_widget = PkgLinks('details')

class RawhideBuildOwner(ContextAwareWidget):
    """
    A widget to display the latest rawhide build and owner for a package.
    """
    params = ['id', 'package', 'build', 'owner']
    template = 'mako:fedoracommunity.mokshaapps.packages.templates.rawhide'

    def update_params(self, d):
        super(RawhideBuildOwner, self).update_params(d)
        koji = get_connector('koji')
        builds = koji._koji_client.getLatestBuilds('dist-rawhide',
                                                   package=d.package)
        d.build = builds[0]['nvr']
        pkgdb = get_connector('pkgdb')
        pkginfo = pkgdb.request_package_info(d.package)
        for pkg in pkginfo[1]['packageListings']:
            if pkg['collection']['branchname'] == 'devel':
                d.owner = pkg['owner']
                break

rawhide_build_and_owner = RawhideBuildOwner('rawhide_build_and_owner')

class OverviewDashboard(PackagesDashboardContainer):
    layout = [Category('content-col-apps', (
                Widget(None, pkg_details_widget,
                       params={'pkg_description': '', 'owner': ''}),
                MokshaApp('',
                    'fedoracommunity.packages/package/rawhide_build_and_owner',
                    params={'package': ''}),
                MokshaApp('Active Releases',
                          'fedoracommunity.updates/table',
                          params={
                              'filters': {
                                  'package': '',
                                  'active_releases': True,
                                  }
                              }),
                Widget('Package Links', pkg_links_widget,
                       params={'package':''}),
                MokshaApp('Latest Changelog Entries',
                          'fedoracommunity.packages/package/changelog/table',
                          params={'filters': {'package': ''},
                              'more_link_code': changelog_links.get_code('CHANGELOG')}),

               ))
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

    @expose('mako:moksha.templates.widget')
    def rawhide_build_and_owner(self, package):
        """ Display the latest rawhide build and owner of a given package """
        tmpl_context.widget = rawhide_build_and_owner
        return dict(options={'package': package})
