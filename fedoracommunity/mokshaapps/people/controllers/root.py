from moksha.lib.base import Controller
from moksha.lib.helpers import Category, MokshaApp, Not, not_anonymous, MokshaWidget
from moksha.api.widgets import ContextAwareWidget, Grid
from moksha.api.widgets.containers import DashboardContainer
from moksha.api.connectors import get_connector

from repoze.what.predicates import not_anonymous
from tg import expose, tmpl_context, require, request

from memberships import MembershipsController
from package_maintenance import PackageMaintenanceController

from uuid import uuid4

class ProfileContainer(DashboardContainer, ContextAwareWidget):
    template='mako:fedoracommunity.mokshaapps.people.templates.peoplecontainer'
    layout = [Category('header-content-column',
                       MokshaApp('', 'fedoracommunity.people/details',params=
                                 {"show_profile": True}
                                 ),
                       css_class='header-content-column'
                       ),
              Category('right-content-column',
                       (MokshaApp('Your Packages', 'fedoracommunity.packages/mypackages'),
                        MokshaApp('Alerts', 'fedoracommunity.alerts'),
                        MokshaApp('Quick Links', 'fedoracommunity.quicklinks')),
                        default_child_css="panel",
                        css_class='right-content-column'
                      ),
              Category('left-content-column',
                       (MokshaApp('Your Group Memberships',
                                 'fedoracommunity.people/memberships/table',
                                 params={"rows_per_page": 5,
                                         "filters":{"profile": True}
                                        }
                                 ),
                        MokshaApp('Your Packages', 'fedoracommunity.packages/mypackages',
                                 params={'view': 'canvas'})
                       ),
                       css_class='left-content-column'
                      )]

class PeopleContainer(DashboardContainer, ContextAwareWidget):
    layout = [Category('header-content-column',
                       MokshaApp('', 'fedoracommunity.people/details',
                                 params={'username':''})
                       ),
              Category('right-content-column',
                        (MokshaApp('Packages', 'fedoracommunity.packages/userpackages',
                                  params={'username':''}),
                         MokshaApp('Alerts', 'fedoracommunity.alerts'),
                         MokshaApp('Quick Links', 'fedoracommunity.quicklinks'))
                        ),
              Category('left-content-column',
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

people_container = PeopleContainer('people_container')
profile_container = ProfileContainer('profile_container')

class RootController(Controller):
    memberships = MembershipsController()
    packagemaint = PackageMaintenanceController()
    @expose('mako:moksha.templates.widget')
    @require(not_anonymous())
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
    @require(not_anonymous())
    def name(self, username, **kwds):

        kwds.update({'u': username})
        return self.index(**kwds)

    @expose('mako:fedoracommunity.mokshaapps.people.templates.info')
    @require(not_anonymous())
    def details(self, username=None, profile=False, compact=False):
        results = {'compact': compact,
                   'id': 'uuid' + str(uuid4())}

        fas_conn = get_connector('fas')
        person = fas_conn.query_userinfo(filters = {'profile': profile,
                                                    'u':username})

        if person:
            person = person[1][0]

        results['person'] = person
        return results

    @expose('mako:fedoracommunity.mokshaapps.people.templates.table')
    @require(not_anonymous())
    def table(self, uid="", rows_per_page=5, filters={}):
        ''' table handler

        This handler displays the main table by itself
        '''

        if isinstance(rows_per_page, basestring):
            rows_per_page = int(rows_per_page)

        tmpl_context.widget = memberships_grid
        return {'filters': filters, 'uid':uid, 'rows_per_page':rows_per_page}
