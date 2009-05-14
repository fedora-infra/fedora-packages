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

from moksha.lib.base import Controller
from moksha.lib.helpers import Category, MokshaApp, Not, not_anonymous, MokshaWidget
from moksha.api.widgets.containers import DashboardContainer
from moksha.api.widgets import ContextAwareWidget
from tg import expose, tmpl_context

from fedoracommunity.mokshaapps.builds.controllers.links import builds_links
from fedoracommunity.mokshaapps.updates.controllers.links import updates_links

class OverviewContainer(DashboardContainer, ContextAwareWidget):
    template = 'mako:fedoracommunity.mokshaapps.overviewresource.templates.overviewcontainer'
    layout = [Category('left-content-column-apps',
                       [MokshaApp('Latest Builds', 'fedoracommunity.builds/table',
                                  params={"rows_per_page": 5,
                                          "more_link_code": builds_links.get_code('ALL_BUILDS'),
                                          "show_owner_filter": True}),
                        MokshaApp('Latest Stable Updates','fedoracommunity.updates/table',
                                  params={
                                      "filters": {
                                          "status":"stable",
                                          "granularity": "minute",
                                          },
                                      "rows_per_page": 5,
                                      "more_link_code": updates_links.get_code('STABLE_UPDATES')}),
                        MokshaApp('Latest Testing Updates','fedoracommunity.updates/table',
                                  params={
                                      "filters": {
                                          "status":"testing",
                                          "granularity": "minute",
                                          },
                                      "rows_per_page": 5,
                                      "more_link_code": updates_links.get_code('TESTING_UPDATES')}),
                        MokshaWidget('Planet Fedora','fedoracommunity.planet', params={'id': 'planet'}),
                        ]
                       ),
              Category('right-content-column-apps',
                       [MokshaWidget(None, 'fedoracommunity.login',
                                     params={'came_from': None},
                                     css_class='',
                                     auth=Not(not_anonymous())),
                        MokshaApp('Alerts', 'fedoracommunity.alerts'),
                        MokshaWidget('Tasks', 'fedoracommunity.quicklinks', auth=not_anonymous()),
                        MokshaApp('My Packages', 'fedoracommunity.packages/mypackages', auth=not_anonymous())
                       ],
                       default_child_css="panel"
                      )
              ]

overview_container = OverviewContainer('overview')

class RootController(Controller):

    @expose('mako:fedoracommunity.mokshaapps.overviewresource.templates.index')
    def index(self):
        tmpl_context.widget = overview_container
        return dict()
