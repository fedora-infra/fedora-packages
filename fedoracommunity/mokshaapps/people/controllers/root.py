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

import logging

from tw.api import Widget
from tg import expose, tmpl_context, require, request, url
from uuid import uuid4
from datetime import datetime
from repoze.what.predicates import not_anonymous
from pytz import utc, timezone

from moksha.lib.base import Controller
from moksha.lib.helpers import Category, MokshaApp, MokshaWidget, DateTimeDisplay
from moksha.api.widgets.feed import Feed
from moksha.api.widgets import ContextAwareWidget, Grid
from moksha.api.connectors import get_connector

from fedoracommunity.widgets.expander import expander_js
from fedoracommunity.widgets.clock import clock_js
from memberships import MembershipsController
from package_maintenance import PackageMaintenanceController

from links import membership_links
from helpers import PeopleDashboardContainer

log = logging.getLogger(__name__)

class ProfileContainer(PeopleDashboardContainer):
    layout = [Category('right-content-column-apps',
                       (MokshaApp('Your Packages', 'fedoracommunity.packages/mypackages'),
                        MokshaApp('Alerts', 'fedoracommunity.alerts'),
                        MokshaWidget('Tasks', 'fedoracommunity.quicklinks', auth=not_anonymous())),
                        default_child_css='app panel',
                        css_class='right-content-column'
                      ),
              Category('left-content-column-apps',
                       (MokshaApp('', 'fedoracommunity.people/details',params=
                                 {'profile': True,
                                  'compact': True}
                                 ),
                        MokshaApp('Your Group Memberships',
                                 'fedoracommunity.people/memberships/table',
                                 params={"rows_per_page": 5,
                                         "filters":{"profile": True},
                                         "more_link_code": membership_links.MEMBERSHIPS.code
                                        }
                                 ),
                        MokshaApp(None,
                                  'fedoracommunity.people/planet',
                                  auth=not_anonymous(),
                                  params={'username': None}),
                       ),
                       css_class='left-content-column'
                      )]

class UserContainer(PeopleDashboardContainer):
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
                                         'compact':True}),
                        MokshaApp('Group Memberships', 'fedoracommunity.people/memberships/table',
                                 params={"rows_per_page": 5,
                                         "more_link_code": membership_links.MEMBERSHIPS.code,
                                         "filters":{"profile": False,
                                                    "username":''}
                                        }
                                 ),
                        MokshaApp(None,
                                  'fedoracommunity.people/planet',
                                  params={'username': None}),
                       ),
                       css_class='left-content-column'
                     )]

class PeopleGrid(Grid, ContextAwareWidget):
    template='mako:fedoracommunity.mokshaapps.people.templates.table_widget'


class PersonDetailsWidget(ContextAwareWidget):
    template = 'mako:fedoracommunity.mokshaapps.people.templates.info'
    params = ['person', 'id', 'compact', 'profile', 'face', 'utc_offset']
    javascript = [expander_js, clock_js]
    face = 'http://planet.fedoraproject.org/images/heads/default.png'

    def update_params(self, d):
        super(PersonDetailsWidget, self).update_params(d)
        d.id = 'uuid' + str(uuid4())

        fas = get_connector('fas')
        person = fas.query_userinfo(filters={
                'profile': d.profile,
                'u': d.username
                })

        if person:
            person = person[1][0]

        d.person = person

        # Get the users hackergochi
        planet = get_connector('planet')
        info = planet.get_user_details(d.person['username'])
        if info:
            d.face = info.get('face', self.face)

        # Determine their UTC offset
        d.utc_offset = ''
        if person.get('timezone'):
            now = datetime.now(utc)
            now = now.astimezone(timezone(person['timezone']))
            offset = now.strftime('%z')
            if offset.startswith('-'):
                offset = offset[1:]
                d.utc_offset += '-'
            hours = int(offset[:2])
            d.utc_offset += str(hours)
            # FIXME: account for minutes?
            #minutes = int(offset[2:])
            #if minutes:
            #    d.utc_offset += '.%d' % ...

class CompactPersonDetailsWidget(PersonDetailsWidget):
    template = 'mako:fedoracommunity.mokshaapps.people.templates.info_compact'

class PersonBlogWidget(Feed, ContextAwareWidget):
    template = 'mako:fedoracommunity.mokshaapps.people.templates.planet'
    javascript = [expander_js]
    params = ['limit', 'username']
    limit = 3
    url = None
    username = None

    def update_params(self, d):
        super(PersonBlogWidget, self).update_params(d)
        for entry in d.entries:
            try:
                entry['last_modified'] = DateTimeDisplay(entry['updated_parsed']).age(general=True) + ' ago'
            except Exception, e:
                log.exception(e)
                log.error("Unable to determine updated timestamp for entry")
                log.error(entry)
                entry['last_modified'] = entry.get('updated', '')


people_grid = PeopleGrid('people_grid')
user_container = UserContainer('user_container')
profile_container = ProfileContainer('profile_container')
person_details_widget = PersonDetailsWidget('person_details_widget')
compact_person_details_widget = CompactPersonDetailsWidget('person_details_widget')

person_blog_widget = PersonBlogWidget('person_blog')

class RootController(Controller):
    memberships = MembershipsController()
    packagemaint = PackageMaintenanceController()
    @expose('mako:moksha.templates.widget')
    def index(self, **kwds):
        options = {
            'username': kwds.get('username', kwds.get('u')),
            'profile': kwds.get('profile')
        }

        if options['profile']:
            tmpl_context.widget = profile_container
            options['username'] = request.identity['repoze.who.userid']
        elif options['username']:
            tmpl_context.widget = user_container
        else:
            pass # todo - make a container for the people list app

        return {'options':options}

    @expose('mako:moksha.templates.widget')
    def name(self, username, **kwds):
        kwds.update({'u': username})
        return self.index(**kwds)

    @expose('mako:moksha.templates.widget')
    def details(self, username=None, profile=False, compact=True):
        if compact:
            tmpl_context.widget = compact_person_details_widget
        else:
            tmpl_context.widget = person_details_widget
        return {'options': {'compact': compact, 'profile': profile,
                            'username': username}}

    @expose('mako:fedoracommunity.mokshaapps.people.templates.table')
    def table(self, rows_per_page=20, filters={}, more_link_code=None):
        ''' table handler

        This handler displays the main table by itself
        '''
        if isinstance(rows_per_page, basestring):
            rows_per_page = int(rows_per_page)

        tmpl_context.widget = people_grid
        return {'filters': filters,
                'rows_per_page':rows_per_page,
                'numericPager': True}

    @expose('mako:moksha.templates.widget')
    def planet(self, username=None):
        options = {}
        planet = get_connector('planet')
        info = planet.get_user_details(username)

        if info:
            options['url'] = info['feed']
            options['username'] = username
            tmpl_context.widget = person_blog_widget
        else:
            tmpl_context.widget = lambda: ''

        return dict(options=options)
