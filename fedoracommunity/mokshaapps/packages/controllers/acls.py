# This file is part of Fedora Community.
# Copyright (C) 2008-2009  Red Hat, Inc.
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

from tg import expose, tmpl_context

from moksha.lib.base import Controller
from moksha.lib.helpers import Category, Widget
from moksha.api.widgets import ContextAwareWidget, Grid

from helpers import PackagesDashboardContainer

class AclsGrid(Grid, ContextAwareWidget):
    template='mako:fedoracommunity.mokshaapps.packages.templates.acls_table_widget'
    resource = 'pkgdb'
    resource_path ='acls'

acls_grid = AclsGrid('acls_grid')

class AclsDashboard(PackagesDashboardContainer):
    template = 'mako:fedoracommunity.mokshaapps.packages.templates.single_col_dashboard'
    layout = [Category('content-col-apps',(Widget('Users', acls_grid,
                                                 params={'rows_per_page': 999999,
                                                         'filters': {'package': '',
                                                                    'roles': ['owner', 'maintainer', 'watcher'],
                                                                    'type': 'users'
                                                                    }
                                                        }
                                                 ),
                                             Widget('Groups', acls_grid,
                                                 params={'rows_per_page': 999999,
                                                         'filters': {'package': '',
                                                                    'roles': ['owner', 'maintainer', 'watcher'],
                                                                    'type': 'groups'
                                                                    }
                                                        }
                                                 )
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
