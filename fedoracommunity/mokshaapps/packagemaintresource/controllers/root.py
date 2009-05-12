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

from moksha.lib.base import Controller
from moksha.lib.helpers import MokshaApp
from tg import expose, tmpl_context
from fedoracommunity.widgets import SubTabbedContainer

class AllPackagesTabbedNav(SubTabbedContainer):
    tabs= (MokshaApp('Packages', 'fedoracommunity.packages'),
           MokshaApp('Builds', 'fedoracommunity.builds'),
           MokshaApp('Updates', 'fedoracommunity.updates'),
          )

class SelectedPackageTabbedNav(SubTabbedContainer):
    tabs= (MokshaApp('Overview', 'fedoracommunity.packages',
                     content_id = 'package_overview',
                     params={'package':''}),
           MokshaApp('Package Details', 'fedoracommunity.packages/details',
                     content_id = 'details',
                     params={'package':''}),
           MokshaApp('Maintenance Tools', 'fedoracommunity.packages/tools',
                     content_id = 'tools',
                     params={'package':''}),
          )

all_packages_nav = AllPackagesTabbedNav('packagemaintnav')
selected_package_nav = SelectedPackageTabbedNav('selectedpackagenav')

class RootController(Controller):

    @expose('mako:moksha.templates.widget')
    def index(self, **kwds):
        options = {}
        package = kwds.get('package')
        tmpl_context.widget = all_packages_nav
        if package:
            options['package'] = package
            tmpl_context.widget = selected_package_nav

        return {'options': options}
