from tg import expose, tmpl_context, require, request
from repoze.what.predicates import not_anonymous

from moksha.lib.base import Controller
from moksha.lib.helpers import Category, MokshaApp, MokshaWidget
from moksha.api.widgets import ContextAwareWidget, Grid
from moksha.api.widgets.containers import DashboardContainer

from fedoracommunity.widgets import SubTabbedContainer
from overview import OverviewController

class UserPkgsCompactGrid(Grid, ContextAwareWidget):
    template='mako:fedoracommunity.mokshaapps.packages.templates.userpkgs_list_widget'

class UserPkgsGrid(Grid, ContextAwareWidget):
    template='mako:fedoracommunity.mokshaapps.packages.templates.userpkgs_table_widget'

class PackageNavContainer(SubTabbedContainer):
    template='mako:fedoracommunity.mokshaapps.packages.templates.package_nav'
    tabs= (Category('',
                    MokshaApp('Overview', 'fedoracommunity.packages/package',
                     params={'package':''})
                   ),
           Category('Package Details',
                    (MokshaApp('Downloads', 'fedoracommunity.packages/package/downloads',
                              params={'package':''}),
                    MokshaApp('Maintainers', 'fedoracommunity.packages/package/acls',
                              params={'package':'',
                                      'roles':"['maintainer']"}),
                    MokshaApp('Owners', 'fedoracommunity.packages/package/acls',
                              params={'package':'',
                                      'roles':"['owner']"}),
                    MokshaApp('Watchers', 'fedoracommunity.packages/package/acls',
                              params={'package':'',
                                      'roles':"['watcher']"}),
                    )
                   ),

           Category('Package Maintenance',
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

class PackagesListContainer(DashboardContainer, ContextAwareWidget):
    layout = [Category('right-content-column',
                        MokshaWidget('Quick Links', 'fedoracommunity.quicklinks', auth=not_anonymous()), default_child_css='panel'),
              Category('left-content-column', # use the builds packages table for now while Toshio fixes the alphaPager json call for pkgdb
                       MokshaApp('All Packages', 'fedoracommunity.builds/packages_table', params={"rows_per_page": 10, "filters":{}}))]

user_pkgs_compact_grid = UserPkgsCompactGrid('usrpkgs_list')
user_pkgs_grid = UserPkgsGrid('usrpkgs_table')

packages_list_container = PackagesListContainer('packages_list_container')
package_nav_container = PackageNavContainer('package_nav_container')

class RootController(Controller):

    package = OverviewController()

    def _user_packages_view(self, username, owner=5, maintainer=3, watcher=False,
                       owner_label='Owned',
                       maintainer_label='Maintained',
                       watcher_label='Watched',
                       rows_per_page=5, morelink=None, view="home"):
        if view=="home":
            categories = []
            if owner:
                owner = int(owner)
                cat = {'label': owner_label,
                       'rows_per_page': owner,
                       'filters':{'owner': True, 'u':username, 'eol': False, 'morelink': False}
                      }
                categories.append(cat)

            if maintainer:
                maintainer = int(maintainer)
                cat = {'label': maintainer_label,
                       'rows_per_page': maintainer,
                       'filters':{'approveacls': True, 'commit': True,'u':username, 'eol': False}
                      }
                categories.append(cat)

            if watcher:
                watcher = int(watcher)
                cat = {'label': watcher_label,
                       'rows_per_page': watcher,
                       'filters':{'watchcommits': True, 'watchbugzilla': True,'u':username, 'eol': False}
                      }
                categories.append(cat)

            tmpl_context.widget = user_pkgs_compact_grid

            return {'categories': categories}
        else:
            rows_per_page = int(rows_per_page)
            tmpl_context.widget = user_pkgs_grid
            return {'categories': None,
                    'filters':{'u':username},
                    'rows_per_page': rows_per_page,
                    }

    @expose('mako:fedoracommunity.mokshaapps.packages.templates.userpackages')
    @require(not_anonymous())
    def mypackages(self, owner=5, maintainer=3, watcher=False,
                   rows_per_page=5, view="home"):
        username = request.identity['repoze.who.userid']

        return self._user_packages_view(username, owner, maintainer, watcher,
                   'Packages I Own', 'Packages I Maintain', 'Packages I Watch',
                   rows_per_page, view)

    @expose('mako:fedoracommunity.mokshaapps.packages.templates.userpackages')
    @require(not_anonymous())
    def userpackages(self, owner=5, maintainer=3, watcher=False, username=None,
                     rows_per_page=5, view='home'):

        return self._user_packages_view(username, owner, maintainer, watcher,
                  'Packages %s Owns' % username,
                  'Packages %s Maintains' % username,
                  'Packages %s Watch' % username,
                   rows_per_page, view)

    # do something for index, this should be the container stuff
    @expose('mako:moksha.templates.widget')
    def index(self, **kwds):
        package = kwds.get('package', None)

        if not package:
            options = {}
            tmpl_context.widget = packages_list_container
        else:
            options = {
                       'package': package
                      }
            tmpl_context.widget = package_nav_container

        return {'options':options}

    @expose('mako:moksha.templates.widget')
    def name(self, pkg_name, **kwds):

        kwds.update({'p': pkg_name})
        return self.index(**kwds)

    @expose('mako:fedoracommunity.mokshaapps.packages.templates.table')
    def table(self, user="", rows_per_page=5, filters={}):
        ''' table handler

        This handler displays the main table by itself
        '''

        if isinstance(rows_per_page, basestring):
            rows_per_page = int(rows_per_page)

        tmpl_context.widget = user_pkgs_grid
        return {'filters': filters, 'uid':user, 'rows_per_page':rows_per_page}
