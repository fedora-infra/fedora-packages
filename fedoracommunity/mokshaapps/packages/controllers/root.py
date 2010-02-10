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

from tg import expose, tmpl_context, require, request
from repoze.what.predicates import not_anonymous

from moksha.lib.base import Controller
from moksha.lib.helpers import Category, MokshaApp, MokshaWidget, Widget, StaticLink
from moksha.api.widgets import ContextAwareWidget, Grid
from moksha.api.widgets.containers import DashboardContainer

from fedoracommunity.widgets import (SubTabbedContainer,
                                    ExtraContentTabbedContainer,
                                    QuickLinksWidget)

from overview import OverviewController

class UserPkgsGrid(Grid, ContextAwareWidget):
    template='mako:fedoracommunity.mokshaapps.packages.templates.userpkgs_table_widget'
    resource='pkgdb'
    resource_path='query_userpackages'
    numericPager=True

class UserPkgsCompactGrid(UserPkgsGrid):
    template='mako:fedoracommunity.mokshaapps.packages.templates.userpkgs_list_widget'

class AllPackagesLinks(QuickLinksWidget):
    links=[('',
           'All Packages',
           '/package_maintenance',
           'all_packages'),
           ('',
           'All Builds',
           '/package_maintenance/builds',
           'all_builds'),
           ('',
           'All Updates',
           '/package_maintenance',
           'all_updates')
          ]

all_packages_links = AllPackagesLinks('all_packages_links')


static_overview_links = Category('',
                    StaticLink('Overview',
                    '/package_maintenance',
                    params={'package':''})
                   )

static_package_detail_links = Category('Package Details',
                    (StaticLink('Downloads', '/package_maintenance/details/downloads',
                              params={'package':''}),
                     StaticLink('Owners', '/package_maintenance/details/owners',
                              params={'package':''}),
                     StaticLink('Maintainers', '/package_maintenance/details/maintainers',
                              params={'package':''}),
                     StaticLink('Watchers', '/package_maintenance/details/watchers',
                              params={'package':''}),
                    )
                   )

static_package_maint_links = Category('Maintenance Tools',
                    (StaticLink('Bugs', '/package_maintenance/tools/bugs',
                              params={'package':''}),
                     StaticLink('Builds', '/package_maintenance/tools/builds',
                              params={'package':''}),
                     StaticLink('Changelog', '/package_maintenance/tools/changelog',
                              params={'package':''}),
                     StaticLink('Sources', '/package_maintenance/tools/sources',
                              params={'package':''}),
                     StaticLink('Updates', '/package_maintenance/tools/updates',
                              params={'package':''}))
                   )

class PackageNavOverviewContainer(ExtraContentTabbedContainer):
    template='mako:fedoracommunity.mokshaapps.packages.templates.package_nav'
    sidebar_apps=(Widget('All Packages', all_packages_links, css_class="app panel"),
                  MokshaWidget('Tasks', 'fedoracommunity.quicklinks', css_class="app panel", auth=not_anonymous()))
    tabs= (Category('',
                    MokshaApp('Overview', 'fedoracommunity.packages/package',
                     params={'package':''})
                   ),
           static_package_detail_links,
           static_package_maint_links
          )

class PackageNavDetailsContainer(ExtraContentTabbedContainer):
    template='mako:fedoracommunity.mokshaapps.packages.templates.package_nav'
    sidebar_apps=(Widget('All Packages', all_packages_links, css_class="app panel"),
                  MokshaWidget('Tasks', 'fedoracommunity.quicklinks', css_class="app panel", auth=not_anonymous()))
    tabs= (static_overview_links,
           Category('Package Details',
                    (MokshaApp('Downloads', 'fedoracommunity.packages/package/downloads',
                              params={'package':''}),
                     MokshaApp('Owners', 'fedoracommunity.packages/package/acls/owners',
                              params={'package':''}),
                     MokshaApp('Maintainers', 'fedoracommunity.packages/package/acls',
                              params={'package':'',
                                      'roles':"['maintainer', 'owners']"}),
                     MokshaApp('Watchers', 'fedoracommunity.packages/package/acls',
                              params={'package':'',
                                      'roles':"['watcher']"}),
                    )
                   ),
           static_package_maint_links
          )

class PackageNavMaintContainer(ExtraContentTabbedContainer):
    template='mako:fedoracommunity.mokshaapps.packages.templates.package_nav'
    sidebar_apps=(Widget('All Packages', all_packages_links, css_class="app panel"),
                  MokshaWidget('Tasks', 'fedoracommunity.quicklinks', css_class="app panel", auth=not_anonymous()))
    tabs= (static_overview_links,
           static_package_detail_links,
           Category('Maintenance Tools',
                    (MokshaApp('Bugs', 'fedoracommunity.packages/package/bugs',
                              params={'package':''}),
                    MokshaApp('Builds', 'fedoracommunity.packages/package/builds',
                              params={'package':''}),
                    MokshaApp('Changelog', 'fedoracommunity.packages/package/changelog',
                              params={'package':''}),
                    MokshaApp('Sources', 'fedoracommunity.packages/package/downloads/source',
                              params={'package':''}),
                    MokshaApp('Updates', 'fedoracommunity.packages/package/updates',
                              params={'package':''}))
                   )
          )

class PackagesListNavContainer(ExtraContentTabbedContainer):
    template = 'mako:fedoracommunity.mokshaapps.packages.templates.package_nav'
    sidebar_apps=(MokshaWidget('Tasks', 'fedoracommunity.quicklinks',
                               auth=not_anonymous(), css_class='app panel'),
                 )
    tabs = (MokshaApp('All Packages', 'fedoracommunity.builds/packages_table',
                                      params={"rows_per_page": 15, "filters":{}}),
            MokshaApp('Packages I Own', 'fedoracommunity.packages/userpackages_table',
                                      params={"rows_per_page": 10,
                                              "filters":{'username': None,
                                                         'owner': True,
                                                         'eol': False
                                                        }
                                             },
                                      auth=not_anonymous()),
            MokshaApp('Packages I Maintain', 'fedoracommunity.packages/userpackages_table',
                                      params={"rows_per_page": 10,
                                              "filters":{'username': None,
                                                         'approveacls': True,
                                                         'commit': True,
                                                         'eol': False
                                                        }
                                             },
                                      auth=not_anonymous()),
            MokshaApp('Packages I Watch', 'fedoracommunity.packages/userpackages_table',
                                      params={"rows_per_page": 10,
                                              "filters":{'username': None,
                                                         'watchcommits': True,
                                                         'watchbugzilla': True,
                                                         'eol': False
                                                        }
                                             },
                                      auth=not_anonymous()),
            )

user_pkgs_compact_grid = UserPkgsCompactGrid('usrpkgs_list')
user_pkgs_grid = UserPkgsGrid('usrpkgs_table')

packages_list_nav_container = PackagesListNavContainer('packages_list_nav_container')
package_nav_overview_container = PackageNavOverviewContainer('selected_package_nav_overview_container')
package_nav_details_container = PackageNavDetailsContainer('selected_package_nav_details_container')
package_nav_maint_container = PackageNavMaintContainer('selected_package_nav_tools_container')

class RootController(Controller):

    package = OverviewController()

    def _user_packages_view(self, username, owner=5, maintainer=3, watcher=False,
                       owner_label='Owned',
                       maintainer_label='Maintained',
                       watcher_label='Watched',
                       rows_per_page=5, more_link_prefix=None, view="home"):
        if view=="home":
            categories = []
            if owner:
                owner = int(owner)

                more_link = None
                if more_link_prefix:
                    more_link = more_link_prefix + '/packages_owned'
                cat = {'label': owner_label,
                       'rows_per_page': owner,
                       'filters':{'owner': True,
                                  'username':username,
                                  'eol': False},
                       'more_link': more_link
                      }
                categories.append(cat)

            if maintainer:
                maintainer = int(maintainer)

                more_link = None
                if more_link_prefix:
                    more_link = more_link_prefix + '/packages_maintained'
                cat = {'label': maintainer_label,
                       'rows_per_page': maintainer,
                       'filters':{'approveacls': True,
                                  'commit': True,
                                  'username':username,
                                  'eol': False},
                       'more_link': more_link
                      }
                categories.append(cat)

            if watcher:
                watcher = int(watcher)

                more_link = None
                if more_link_prefix:
                    more_link = more_link_prefix + '/packages_watched'
                cat = {'label': watcher_label,
                       'rows_per_page': watcher,
                       'filters':{'watchcommits': True,
                                  'watchbugzilla': True,
                                  'username':username,
                                  'eol': False},
                       'more_link': more_link
                      }
                categories.append(cat)

            tmpl_context.widget = user_pkgs_compact_grid

            return {'categories': categories}
        else:
            rows_per_page = int(rows_per_page)
            tmpl_context.widget = user_pkgs_grid

            more_link = None
            if more_link_prefix:
                more_link = more_link_prefix

            return {'categories': None,
                    'filters':{'username':username},
                    'rows_per_page': rows_per_page
                    }

    @expose('mako:fedoracommunity.mokshaapps.packages.templates.userpackages')
    @require(not_anonymous())
    def mypackages(self, owner=5, maintainer=3, watcher=False,
                   rows_per_page=5, view="home"):
        username = request.identity['repoze.who.userid']

        return self._user_packages_view(username, owner, maintainer, watcher,
                   'Packages I Own',
                   'Packages I Maintain',
                   'Packages I Watch',
                   rows_per_page,
                   '/my_profile/package_maintenance',
                   view)

    @expose('mako:fedoracommunity.mokshaapps.packages.templates.userpackages')
    def userpackages(self, owner=5, maintainer=3, watcher=False, username=None,
                     rows_per_page=5, view='home'):

        return self._user_packages_view(username, owner, maintainer, watcher,
                  'Packages %s Owns' % username,
                  'Packages %s Maintains' % username,
                  'Packages %s Watch' % username,
                   rows_per_page, '/people/package_maintenance',
                   view)

    @expose('mako:fedoracommunity.mokshaapps.packages.templates.userpackages')
    def userpackages_table(self, filters=None, rows_per_page=10, title=''):
        if filters==None:
            filters = {}

        tmpl_context.widget = user_pkgs_grid
        return {'filters': filters,
                'rows_per_page':rows_per_page,
                'title': title}

    @expose('mako:moksha.templates.widget')
    def index(self, **kwds):
        package = kwds.get('package', None)

        if not package:
            username = ''
            if request.identity:
                username = request.identity.get('repoze.who.userid', '')
            options = {'username': username}
            tmpl_context.widget = packages_list_nav_container
        else:
            options = {
                       'package': package
                      }
            tmpl_context.widget = package_nav_overview_container

        return {'options':options}

    @expose('mako:moksha.templates.widget')
    def details(self, *args, **kwds):
        package = kwds.get('package', None)
        options = {'package': package}
        tmpl_context.widget = package_nav_details_container

        return {'options': options}

    @expose('mako:moksha.templates.widget')
    def tools(self, *args, **kwds):
        package = kwds.get('package', None)
        options = {'package': package}
        tmpl_context.widget = package_nav_maint_container

        return {'options': options}

    @expose('mako:moksha.templates.widget')
    def name(self, pkg_name, **kwds):

        kwds.update({'p': pkg_name})
        return self.index(**kwds)

    @expose('mako:fedoracommunity.mokshaapps.packages.templates.table')
    def table(self, rows_per_page=5, filters={}):
        ''' table handler

        This handler displays the main table by itself
        '''

        if isinstance(rows_per_page, basestring):
            rows_per_page = int(rows_per_page)

        tmpl_context.widget = user_pkgs_grid
        return {'filters': filters, 'rows_per_page':rows_per_page}
