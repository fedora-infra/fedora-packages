from tg import expose, tmpl_context, require
from repoze.what.predicates import not_anonymous

from moksha.lib.base import Controller
from moksha.lib.helpers import Category, MokshaApp, MokshaWidget
from moksha.api.widgets import ContextAwareWidget
from moksha.api.widgets.containers import DashboardContainer

from fedoracommunity.widgets import ExtraContentTabbedContainer

from fedoracommunity.mokshaapps.builds.controllers.root import (
    in_progress_builds_app,
    failed_builds_app,
    successful_builds_app,
    overview_builds_app)

from fedoracommunity.mokshaapps.updates.controllers.root import (
    unpushed_updates_app,
    testing_updates_app,
    stable_updates_app,
    overview_updates_app)

class PeopleNavContainer(ExtraContentTabbedContainer):
    template='mako:fedoracommunity.mokshaapps.people.templates.people_package_nav'
    sidebar_apps = (MokshaApp('Alerts', 'fedoracommunity.alerts',
                              params={'username':None},
                              css_class='app panel'),)
    header_apps = (MokshaApp('', 'fedoracommunity.people/details',
                                params={'compact': True,
                                        'username': None}),)

    tabs= (Category('Builds',
                    (overview_builds_app.clone({'username': None}),
                     in_progress_builds_app.clone({'filters':{'username':None}}),
                     failed_builds_app.clone({'filters':{'username':None}}),
                     successful_builds_app.clone({'filters':{'username':None}})),
                    ),

           Category('Updates',
                    (overview_updates_app.clone({'username':None}),
                     unpushed_updates_app.clone({'filters':{'username':None}}),
                     testing_updates_app.clone({'filters':{'username':None}}),
                     stable_updates_app.clone({'filters':{'username':None}}))
                   )
          )

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

people_nav_container  = PeopleNavContainer('package_maint_people_nav_container')


class PackageMaintenanceController(Controller):
    @expose('mako:moksha.templates.widget')
    def index(self, **kwds):
        options = {
            'username': kwds.get('username', kwds.get('u')),
            'profile': kwds.get('profile')
        }

        if options['profile']:
            tmpl_context.widget = profile_memberships_container
        elif options['username']:
            tmpl_context.widget = people_nav_container

        return {'options': options}
