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

from pylons import cache
from fedora.client import Wiki
from datetime import datetime, timedelta
from moksha.api.widgets import Grid
from moksha.api.widgets.containers import DashboardContainer
from moksha.lib.helpers import Category, Widget as MokshaWidget, defaultdict
from moksha.api.connectors import get_connector
from fedoracommunity.widgets.flot import FlotWidget
import simplejson

class NumPackagesPerCollection(FlotWidget):

    def update_params(self, d):
        pkgdb_connector = get_connector('pkgdb')
        pkgdb_cache = cache.get_cache('wiki')
        flot = pkgdb_cache.get_value(key='num_pkgs_per_collection',
                createfunc=pkgdb_connector.get_num_pkgs_per_collection,
                expiretime=1800)
        d.data = simplejson.dumps([{'data': [(0, 0)] + flot['data'],
                                    'lines': {'show': True}}])
        d.options = simplejson.dumps(flot['options'])
        d.label = 'The number of packages in Fedora per release'
        d.tooltips = True
        d.width = '500px'
        super(NumPackagesPerCollection, self).update_params(d)


num_pkgs_per_collection = NumPackagesPerCollection('num_pkgs_per_collection')


class PackageStatisticsDashboard(DashboardContainer):
    layout = [
            Category('left-content-column-apps', [
                MokshaWidget('Number of packages in Fedora', num_pkgs_per_collection),
            ]),
    ]

package_stats_dashboard = PackageStatisticsDashboard('package_stats')
