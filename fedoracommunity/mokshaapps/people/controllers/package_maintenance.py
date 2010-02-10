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

from tg import expose, tmpl_context, require, validate
from formencode import validators
from repoze.what.predicates import not_anonymous

from moksha.lib.base import Controller
from moksha.lib.helpers import Category, MokshaApp, MokshaWidget
from moksha.api.widgets import ContextAwareWidget
from moksha.api.widgets.containers import DashboardContainer

from fedoracommunity.widgets import ExtraContentTabbedContainer

from helpers import PeopleDashboardContainer

from fedoracommunity.mokshaapps.builds.controllers.root import (
    in_progress_builds_app,
    failed_builds_app,
    successful_builds_app)

from fedoracommunity.mokshaapps.builds.controllers.links import people_builds_links, profile_builds_links

from fedoracommunity.mokshaapps.updates.controllers.root import (
    unpushed_updates_app,
    testing_updates_app,
    stable_updates_app,
    overview_updates_app)

class PeopleBuildsOverviewContainer(DashboardContainer, ContextAwareWidget):
    layout = [Category('group-1-apps',
                        (in_progress_builds_app.clone({'rows_per_page': 5,
                                                       'title_level': 3,
                                                       'more_link_code': people_builds_links.IN_PROGRESS.code},
                                                      label='',
                                                      content_id='in_progress_builds'),
                        failed_builds_app.clone({'rows_per_page': 5,
                                                 'title_level': 3,
                                                 'more_link_code': people_builds_links.FAILED.code},
                                                label='',
                                                content_id='failed_builds'))
                      ),
              Category('group-2-apps',
                       successful_builds_app.clone({'rows_per_page': 5,
                                                    'title_level': 3,
                                                       'more_link_code': people_builds_links.SUCCESSFUL.code},
                                                    label='',
                                                    content_id='successful_builds')
                      )
             ]

people_builds_overview_container = PeopleBuildsOverviewContainer('people_builds_overview')

class ProfileBuildsOverviewContainer(DashboardContainer, ContextAwareWidget):
    layout = [Category('group-1-apps',
                        (in_progress_builds_app.clone({'rows_per_page': 5,
                                                       'more_link_code': profile_builds_links.IN_PROGRESS.code,
                                                       'title_level': 3},
                                                      label='',
                                                      content_id='in_progress_builds'),
                        failed_builds_app.clone({'rows_per_page': 5,
                                                 'more_link_code': profile_builds_links.FAILED.code,
                                                 'title_level': 3},
                                                label='',
                                                content_id='failed_builds'))
                      ),
              Category('group-2-apps',
                       successful_builds_app.clone({'rows_per_page': 5,
                                                    'more_link_code': profile_builds_links.SUCCESSFUL.code,
                                                    'title_level': 3},
                                                   label='',
                                                   content_id='successful')
                      )
             ]

profile_builds_overview_container = ProfileBuildsOverviewContainer('profile_builds_overview')



packages_owned_app = MokshaApp('Packages Owned',
                               'fedoracommunity.packages/userpackages_table',
                               params={'filters':{'username': '',
                                                  'owner': True,
                                                  'eol': False},
                                       'rows_per_page': 25})

packages_maintained_app = MokshaApp('Packages Maintained',
                               'fedoracommunity.packages/userpackages_table',
                               params={'filters':{'approveacls': True,
                                                  'commit': True,
                                                  'username': '',
                                                  'eol': False},
                                       'rows_per_page': 25})
packages_watched_app = MokshaApp('Packages Watched',
                               'fedoracommunity.packages/userpackages_table',
                               params={'filters':{'watchcommits': True,
                                                  'watchbugzilla': True,
                                                  'username': '',
                                                  'eol': False},
                                       'rows_per_page': 25})


class ProfileNavContainer(ExtraContentTabbedContainer, PeopleDashboardContainer):
    template='mako:fedoracommunity.mokshaapps.people.templates.people_package_nav'
    sidebar_apps = (MokshaApp('Alerts', 'fedoracommunity.alerts',
                              params={'profile':True},
                              css_class='app panel'),
                    MokshaWidget('Tasks', 'fedoracommunity.quicklinks', css_class="app panel", auth=not_anonymous()))
    header_apps = (MokshaApp('', 'fedoracommunity.people/details',
                                params={'compact': True,
                                        'profile': True}),)

    tabs= (Category('Packages',
                    (packages_owned_app.clone({'filters':{'profile': True},
                                               'title': 'Packages I Own'}),
                     packages_maintained_app.clone({'filters':{'profile': True},
                                                    'title': 'Packages I Maintain'
                                              }),
                     packages_watched_app.clone({'filters':{'profile': True},
                                                 'title': 'Packages I Watch'
                                              })
                     )
                    ),
           Category('Builds',
                    (MokshaApp('Overview', 'fedoracommunity.people/packagemaint/builds_overview', params={'profile': True}, content_id='builds_overview'),
                     in_progress_builds_app.clone({'filters':{'profile':True}, 'title_level': 3}, content_id='builds_inprogress'),
                     failed_builds_app.clone({'filters':{'profile':True}, 'title_level': 3}, content_id='builds_failed'),
                     successful_builds_app.clone({'filters':{'profile':True}, 'title_level': 3}, content_id='builds_succeeded')),
                    ),

           Category('Updates',
                    (overview_updates_app.clone({'profile':True,
                                                 'title_level': 3}),
                     unpushed_updates_app.clone({'filters':{'profile':True},
                                                 'title_level': 3}),
                     testing_updates_app.clone({'filters':{'profile':True},
                                                'title_level': 3}),
                     stable_updates_app.clone({'filters':{'profile':True},
                                               'title_level': 3}))
                   )
          )

class PeopleNavContainer(ExtraContentTabbedContainer, PeopleDashboardContainer):
    template='mako:fedoracommunity.mokshaapps.people.templates.people_package_nav'
    sidebar_apps = (MokshaApp('Alerts', 'fedoracommunity.alerts',
                              params={'username':None},
                              css_class='app panel'),)
    header_apps = (MokshaApp('', 'fedoracommunity.people/details',
                                params={'compact': True,
                                        'username': None}),)

    tabs= (Category('Packages',
                    (packages_owned_app.clone({'title': 'Packages Owned'}),
                     packages_maintained_app.clone({'title': 'Packages Maintained'}),
                     packages_watched_app.clone({'title': 'Packages Watched'})
                     )
                    ),
           Category('Builds',
                    (MokshaApp('Overview', 'fedoracommunity.people/packagemaint/builds_overview', params={'username': None}, content_id='builds_overview'),
                     in_progress_builds_app.clone({'filters':{'username':None}, 'title_level': 3}, content_id='builds_inprogress'),
                     failed_builds_app.clone({'filters':{'username':None}, 'title_level': 3}, content_id='builds_failed'),
                     successful_builds_app.clone({'filters':{'username':None}, 'title_level': 3}, content_id='builds_succeeded')),
                    ),

           Category('Updates',
                    (overview_updates_app.clone({'username':None,
                                                 'title_level': 3}),
                     unpushed_updates_app.clone({'filters':{'username':None},
                                                 'title_level': 3}),
                     testing_updates_app.clone({'filters':{'username':None},
                                                'title_level': 3}),
                     stable_updates_app.clone({'filters':{'username':None},
                                               'title_level': 3}))
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

    @expose('mako:moksha.templates.widget')
    @validate({'profile': validators.StringBool()})
    def builds_overview(self, profile=False, username=None):
        if profile:
            options = {'profile': True}
            tmpl_context.widget = profile_builds_overview_container
        else:
            options = {'username': username}
            tmpl_context.widget = people_builds_overview_container

        return {'options': options}
