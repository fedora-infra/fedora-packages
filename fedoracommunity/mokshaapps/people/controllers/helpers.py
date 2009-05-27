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

from moksha.api.widgets import ContextAwareWidget
from moksha.api.widgets.containers import DashboardContainer

from moksha.api.connectors import get_connector

class PeopleDashboardContainer(DashboardContainer, ContextAwareWidget):
    template='mako:fedoracommunity.mokshaapps.people.templates.peoplecontainer'

    def update_params(self, d):
        # get the user details
        user = d.get('username')
        profile = d.get('profile')

        conn = get_connector('fas')
        person = conn.query_userinfo(filters={
                'profile': profile,
                'u': user
                })[1]


        if 'error_type' in person:
            d['error'] = person['error']
            d['error_type'] = person['error_type']
            d['human_name'] = 'Unknown User (%s)' % user
        else:
            d['human_name'] = person[0]['human_name']

        super(PeopleDashboardContainer, self).update_params(d)