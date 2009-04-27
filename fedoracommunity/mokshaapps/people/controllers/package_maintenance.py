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

packages_owned_app = MokshaApp('Packages Owned',
                               'fedoracommunity.packages/userpackages_table',
                               params={'filters':{'username': '',
                                                  'owner': True,
                                                  'eol': False}})

packages_maintained_app = MokshaApp('Packages Maintained',
                               'fedoracommunity.packages/userpackages_table',
                               params={'filters':{'approveacls': True,
                                                  'commit': True,
                                                  'username': '',
                                                  'eol': False}})
packages_watched_app = MokshaApp('Packages Watched',
                               'fedoracommunity.packages/userpackages_table',
                               params={'filters':{'watchcommits': True,
                                                  'watchbugzilla': True,
                                                  'username': '',
                                                  'eol': False}})


class ProfileNavContainer(ExtraContentTabbedContainer):
    template='mako:fedoracommunity.mokshaapps.people.templates.people_package_nav'
    sidebar_apps = (MokshaApp('Alerts', 'fedoracommunity.alerts',
                              params={'profile':True},
                              css_class='app panel'),)
    header_apps = (MokshaApp('', 'fedoracommunity.people/details',
                                params={'compact': True,
                                        'profile': True}),)

    tabs= (Category('Packages',
                    (packages_owned_app.clone({'filters':{'profile': True}
                                              }),
                     packages_maintained_app.clone({'filters':{'profile': True}
                                              }),
                     packages_watched_app.clone({'filters':{'profile': True}
                                              })
                     )
                    ),
           Category('Builds',
                    (overview_builds_app.clone({'profile': True}),
                     in_progress_builds_app.clone({'filters':{'profile':True}}),
                     failed_builds_app.clone({'filters':{'profile':True}}),
                     successful_builds_app.clone({'filters':{'profile':True}})),
                    ),

           Category('Updates',
                    (overview_updates_app.clone({'profile':True}),
                     unpushed_updates_app.clone({'filters':{'profile':True}}),
                     testing_updates_app.clone({'filters':{'profile':True}}),
                     stable_updates_app.clone({'filters':{'profile':True}}))
                   )
          )

class PeopleNavContainer(ExtraContentTabbedContainer):
    template='mako:fedoracommunity.mokshaapps.people.templates.people_package_nav'
    sidebar_apps = (MokshaApp('Alerts', 'fedoracommunity.alerts',
                              params={'username':None},
                              css_class='app panel'),)
    header_apps = (MokshaApp('', 'fedoracommunity.people/details',
                                params={'compact': True,
                                        'username': None}),)

    tabs= (Category('Packages',
                    (packages_owned_app,
                     packages_maintained_app,
                     packages_watched_app
                     )
                    ),
           Category('Builds',
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

people_nav_container  = PeopleNavContainer('package_maint_people_nav_container')
profile_nav_container = ProfileNavContainer('package_maint_profile_nav_container')

class PackageMaintenanceController(Controller):
    @expose('mako:moksha.templates.widget')
    def index(self, **kwds):
        options = {
            'username': kwds.get('username', kwds.get('u')),
            'profile': kwds.get('profile')
        }

        if options['profile']:
            tmpl_context.widget = profile_nav_container
        elif options['username']:
            tmpl_context.widget = people_nav_container

        return {'options': options}
