from tg import expose, tmpl_context

from moksha.lib.base import Controller
from moksha.lib.helpers import Category, Widget
from moksha.api.widgets import ContextAwareWidget, Grid

from helpers import PackagesDashboardContainer

class AclsGrid(Grid, ContextAwareWidget):
    template='mako:fedoracommunity.mokshaapps.packages.templates.acls_table_widget'

    def update_params(self, d):
        d['resource'] = 'pkgdb',
        d['resource_path'] = 'acls'
        super(AclsGrid, self).update_params(d)

acls_grid = AclsGrid('acls_grid')

class AclsDashboard(PackagesDashboardContainer):
    template = 'mako:fedoracommunity.mokshaapps.packages.templates.single_col_dashboard'
    layout = [Category('content-col-apps',Widget('Users', acls_grid,
                                                 params={'rows_per_page': 10,
                                                         'filters': {'package': '',
                                                                    'roles': ['owner', 'maintainer', 'watcher']
                                                                    }
                                                        }
                                                 )
                      )
             ]

acls_dashboard = AclsDashboard('acl_dashboard')

class AclsController(Controller):
    @expose('mako:moksha.templates.widget')
    def index(self, package, roles=None):
        if not roles:
            roles = ['owner', 'maintainer', 'watcher']
        tmpl_context.widget = acls_dashboard
        return {'options':{'package': package, 'roles': roles}}

