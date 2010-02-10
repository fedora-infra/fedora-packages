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

from moksha.api.widgets.containers import DashboardContainer
from moksha.api.widgets import ContextAwareWidget
from moksha.api.connectors import get_connector

class PackagesDashboardContainer(DashboardContainer, ContextAwareWidget):
    template = 'mako:fedoracommunity.mokshaapps.packages.templates.single_col_dashboard'

    def update_params(self, d):
        # get the package description
        p = d.get('package')
        conn = get_connector('pkgdb')
        info = conn.get_basic_package_info(p)

        if 'error_type' in info:
            d['error'] = info['error']
            d['error_type'] = info['error_type']
            d['pkg_description'] = ''
            d['pkg_summary'] = 'Unknown Package'
        else:
            d['pkg_description'] = info['description']
            d['pkg_summary'] = info['summary']

        super(PackagesDashboardContainer, self).update_params(d)