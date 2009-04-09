from moksha.lib.base import Controller
from moksha.lib.helpers import Category, MokshaApp, Not, not_anonymous, MokshaWidget
from moksha.api.widgets import ContextAwareWidget, Grid
from moksha.api.widgets.containers import DashboardContainer

from repoze.what.predicates import not_anonymous
from tg import expose, tmpl_context, require, request

class ProfileContainer(DashboardContainer, ContextAwareWidget):
    layout = [Category('header-content-column',
                       MokshaApp('', 'fedoracommunity.people/details',
                                 params={'compact': True,
                                         'profile': True}),
                       css_class='header-content-column'
                       ),
              Category('right-content-column',
                       (MokshaApp('Your Packages', 'fedoracommunity.packages/mypackages'),
                        MokshaApp('Alerts', 'fedoracommunity.alerts'),
                        MokshaWidget('Quick Links', 'fedoracommunity.quicklinks', auth=not_anonymous())),
                        default_child_css='panel',
                        css_class='right-content-column'
                      ),
              Category('left-content-column',
                       (MokshaApp('Your Packages',
                                 'fedoracommunity.packages/mypackages',
                                 params={'rows_per_page': 10,
                                         'view': 'canvas'
                                        }
                                 ),

                       ),
                       css_class='left-content-column'
                      )]

class PeopleContainer(DashboardContainer, ContextAwareWidget):
    layout = [Category('header-content-column',
                       MokshaApp('', 'fedoracommunity.people/details',
                                 params={'username':'',
                                         'compact': True})
                       ),
              Category('right-content-column',
                        (MokshaApp('Packages', 'fedoracommunity.packages/userpackages',
                                  params={'username':''}),
                         MokshaApp('Alerts', 'fedoracommunity.alerts'),
                         MokshaWidget('Quick Links', 'fedoracommunity.quicklinks', auth=not_anonymous()))
                        ),
              Category('left-content-column',
                       (MokshaApp('Packages', 'fedoracommunity.packages/userpackages',
                                 params={'rows_per_page': 10,
                                         'username':'',
                                         'view': 'canvas'
                                        }
                                 ),
                        )
                       )]

people_memberships_container = PeopleContainer('people_memberships_container')
profile_memberships_container = ProfileContainer('profile_memberships_container')

class PackageMaintenanceController(Controller):
    @expose('mako:moksha.templates.widget')
    @require(not_anonymous())
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