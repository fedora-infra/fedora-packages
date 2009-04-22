from tw.api import Widget
from tg import expose, tmpl_context, require, request
from uuid import uuid4
from datetime import datetime
from repoze.what.predicates import not_anonymous

from moksha.lib.base import Controller
from moksha.lib.helpers import Category, MokshaApp, MokshaWidget
from moksha.api.widgets.feed import Feed
from moksha.api.widgets import ContextAwareWidget, Grid
from moksha.api.widgets.containers import DashboardContainer
from moksha.api.connectors import get_connector
from moksha.connector.utils import DateTimeDisplay

from fedoracommunity.widgets.expander import expander_js
from memberships import MembershipsController
from package_maintenance import PackageMaintenanceController

class ProfileContainer(DashboardContainer, ContextAwareWidget):
    template='mako:fedoracommunity.mokshaapps.people.templates.peoplecontainer'
    layout = [Category('header-content-column-apps',
                       MokshaApp('', 'fedoracommunity.people/details',params=
                                 {"profile": True}
                                 ),
                       ),
              Category('right-content-column-apps',
                       (MokshaApp('Your Packages', 'fedoracommunity.packages/mypackages'),
                        MokshaApp('Alerts', 'fedoracommunity.alerts'),
                        MokshaWidget('Quick Links', 'fedoracommunity.quicklinks', auth=not_anonymous())),
                        default_child_css="panel",
                      ),
              Category('left-content-column-apps',
                       (MokshaApp('Your Group Memberships',
                                 'fedoracommunity.people/memberships/table',
                                 params={"rows_per_page": 5,
                                         "filters":{"profile": True}
                                        }
                                 ),
                        MokshaApp('Your Latest Blog Posts',
                                  'fedoracommunity.people/planet',
                                  params={'username': None}),
                        MokshaApp('Your Packages', 'fedoracommunity.packages/mypackages',
                                 params={'view': 'canvas'})
                       ),
                      )]

class PeopleContainer(DashboardContainer, ContextAwareWidget):
    layout = [Category('header-content-column-apps',
                       MokshaApp('', 'fedoracommunity.people/details',
                                 params={'username':''})
                       ),
              Category('right-content-column-apps',
                        (MokshaApp('Packages', 'fedoracommunity.packages/userpackages',
                                  params={'username':''}),
                         MokshaApp('Alerts', 'fedoracommunity.alerts'),
                         MokshaWidget('Quick Links', 'fedoracommunity.quicklinks', auth=not_anonymous()))
                        ),
              Category('left-content-column-apps',
                       (MokshaApp('Group Memberships', 'fedoracommunity.people/memberships/table',
                                 params={"rows_per_page": 5,
                                         "filters":{"profile": False,
                                                    "username":''}
                                        }
                                 ),
                        MokshaApp('Packages', 'fedoracommunity.packages/userpackages',
                                 params={'view': 'canvas',
                                         'username': ''})
                        )
                       )]

class PeopleGrid(Grid, ContextAwareWidget):
    template='mako:fedoracommunity.mokshaapps.people.templates.table_widget'


class PersonDetailsWidget(Widget):
    template = 'mako:fedoracommunity.mokshaapps.people.templates.info'
    params = ['person', 'id', 'compact', 'profile']
    javascript = [expander_js]

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


class PersonBlogWidget(Feed):
    template = 'mako:fedoracommunity.mokshaapps.people.templates.planet'
    javascript = [expander_js]
    params = ['limit']
    limit = 3
    url = None

    def update_params(self, d):
        super(PersonBlogWidget, self).update_params(d)
        for entry in d.entries:
            updated = datetime(*entry['updated_parsed'][:-2])
            entry['last_modified']= DateTimeDisplay(updated).when(0)['when']


people_grid = PeopleGrid('people_grid')
people_container = PeopleContainer('people_container')
profile_container = ProfileContainer('profile_container')
person_details_widget = PersonDetailsWidget('person_details_widget')
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
        elif options['username']:
            tmpl_context.widget = people_container
        else:
            pass # todo - make a container for the people list app

        return {'options':options}

    @expose('mako:moksha.templates.widget')
    def name(self, username, **kwds):

        kwds.update({'u': username})
        return self.index(**kwds)

    @expose('mako:moksha.templates.widget')
    def details(self, username=None, profile=False, compact=False):
        tmpl_context.widget = person_details_widget
        return {'options': {'compact': compact, 'profile': profile,
                            'username': username}}

    @expose('mako:fedoracommunity.mokshaapps.people.templates.table')
    def table(self, rows_per_page=10, filters={}, more_link_code=None):
        ''' table handler

        This handler displays the main table by itself
        '''

        if isinstance(rows_per_page, basestring):
            rows_per_page = int(rows_per_page)

        tmpl_context.widget = people_grid
        return {'filters': filters,
                'rows_per_page':rows_per_page,
                'more_link': None}

    @expose('mako:moksha.templates.widget')
    @require(not_anonymous())
    def planet(self):
        username = request.identity['repoze.who.userid']
        planet = get_connector('planet')
        info = planet.get_user_details(username)
        tmpl_context.widget = person_blog_widget
        return dict(options={'url': info['feed']})
