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

from pylons import config
from fedora.client import Wiki
from datetime import datetime, timedelta
from moksha.api.widgets import Grid
from moksha.api.widgets.containers import DashboardContainer
from moksha.lib.helpers import Category, Widget as MokshaWidget, defaultdict
from moksha.api.connectors import get_connector
from fedoracommunity.widgets.flot import FlotWidget
from shove import Shove
import simplejson

class ClaDoneOverTime(FlotWidget):
    # This is the magic time (in microseconds since the UNIX Epoch) that Toshio
    # gave me where the end of the initial FAS2 import lies. Any timestamps
    # prior to this can't be trusted.
    # start_date = "2008-03-12 02:06:00"
    start_date = 1205305560000

    def __init__(self, *args, **kwargs):
        self.width = "500px"
        super(ClaDoneOverTime, self).__init__(*args, **kwargs)

    def update_params(self, d):
        fas_connector = get_connector('fas')
        stats_cache = Shove(config.get('stats_cache'))
        if 'group_membership_cla_done' in stats_cache.keys():
            data = stats_cache['group_membership_cla_done']
        else:
            data = fas_connector.group_membership_over_time()
        d.data = simplejson.dumps([data])
        d.options = {'xaxis': {'mode': 'time', 'min': self.start_date}}
        super(ClaDoneOverTime, self).update_params(d)


cla_done_over_time = ClaDoneOverTime('cla_done_over_time')


class AccountsStatisticsDashboard(DashboardContainer):
    layout = [
            Category('left-content-column-apps', [
                MokshaWidget('cla_done members over time', cla_done_over_time),
                ]),
    ]

fas_stats_dashboard = AccountsStatisticsDashboard('fas_stats')
