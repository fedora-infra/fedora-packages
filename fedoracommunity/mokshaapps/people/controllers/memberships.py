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

from tg import expose, tmpl_context, require
from repoze.what.predicates import not_anonymous
from paste.deploy.converters import asbool

from moksha.lib.base import Controller
from moksha.lib.helpers import Category, MokshaApp, MokshaWidget
from moksha.api.widgets import ContextAwareWidget, Grid
from moksha.api.widgets.containers import DashboardContainer

from links import membership_links, profile_membership_links
from helpers import PeopleDashboardContainer
import simplejson as json

class UserMembershipsGrid(Grid, ContextAwareWidget):
    template='mako:fedoracommunity.mokshaapps.people.templates.memberships_table_widget'

class ProfileContainer(PeopleDashboardContainer):
    layout = [Category('right-content-column-apps',
                       (MokshaApp('Your Packages', 'fedoracommunity.packages/mypackages'),
                        MokshaApp('Alerts', 'fedoracommunity.alerts'),
                        MokshaWidget('Tasks', 'fedoracommunity.quicklinks', auth=not_anonymous())),
                        default_child_css="app panel",
                        css_class='right-content-column'
                      ),
              Category('left-content-column-apps',
                       (MokshaApp('', 'fedoracommunity.people/details',
                                 params={'compact': True,
                                         'profile': True}),
                        MokshaApp('Your Group Memberships',
                                 'fedoracommunity.people/memberships/table',
                                 params={"rows_per_page": 10,
                                         "filters":{"profile": True,
                                                    "unapproved": False}
                                        }
                                 ),
                        MokshaApp('Your Unapproved Group Memberships',
                                 'fedoracommunity.people/memberships/table',
                                 params={"rows_per_page": 5,
                                         "filters":{"profile": True,
                                                    "approved": False}
                                        }
                                 )
                       ),
                       css_class='left-content-column'
                      )]

class PeopleContainer(PeopleDashboardContainer):
    layout = [Category('right-content-column-apps',
                        (MokshaApp('Packages', 'fedoracommunity.packages/userpackages',
                                  params={'username':''}),
                         MokshaApp('Alerts', 'fedoracommunity.alerts'),
                         MokshaWidget('Tasks', 'fedoracommunity.quicklinks', auth=not_anonymous())),
                         default_child_css='app panel',
                         css_class='right-content-column'
                        ),
              Category('left-content-column-apps',
                       (MokshaApp('', 'fedoracommunity.people/details',
                                 params={'username':'',
                                         'compact': True}),
                       MokshaApp('Group Memberships', 'fedoracommunity.people/memberships/table',
                                 params={"rows_per_page": 10,
                                         "filters":{"username":'',
                                                    "unapproved": False}
                                        }
                                 ),

                        MokshaApp('Unapproved Group Memberships', 'fedoracommunity.people/memberships/table',
                                 params={"rows_per_page": 5,
                                         "filters":{"username":'',
                                                    "approved": False}
                                        }
                                 ),
                        ),
                        css_class='left-content-column'
                       )]

memberships_grid = UserMembershipsGrid('user_memberships')
people_memberships_container = PeopleContainer('people_memberships_container')
profile_memberships_container = ProfileContainer('profile_memberships_container')

class MembershipsController(Controller):
    @expose('mako:moksha.templates.widget')
    def index(self, **kwds):
        options = {
            'username': kwds.get('username', kwds.get('u')),
            'profile': kwds.get('profile')
        }

        if options['profile']:
            tmpl_context.widget = profile_memberships_container
        elif options['username']:
            tmpl_context.widget = people_memberships_container

        return {'options': options}

    @expose('mako:fedoracommunity.mokshaapps.people.templates.memberships_table')
    def table(self, rows_per_page=5, filters=None, more_link_code=None):
        if isinstance(rows_per_page, basestring):
            rows_per_page = int(rows_per_page)

        if filters == None:
            filters = {}

        more_link = None
        if more_link_code:
            if isinstance(filters, basestring):
                decoded_filters = json.loads(filters)
            else:
                decoded_filters = filters

            if asbool(decoded_filters.get('profile')) == True:
                more_link = profile_membership_links.get_data(more_link_code)
            else:
                more_link = membership_links.get_data(more_link_code)

        tmpl_context.widget = memberships_grid
        return {'filters': filters,
                'rows_per_page':rows_per_page,
                'more_link': more_link}
