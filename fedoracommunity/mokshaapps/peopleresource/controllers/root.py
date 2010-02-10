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

from moksha.lib.base import Controller
from moksha.lib.helpers import MokshaApp, MokshaWidget, Category, Not, not_anonymous
from moksha.api.widgets.containers import DashboardContainer
from tg import expose, tmpl_context
from fedoracommunity.widgets import SubTabbedContainer

class NameTabbedNav(SubTabbedContainer):
    tabs = (MokshaApp('Info', 'fedoracommunity.people',
                      params={'username':None}),
            MokshaApp('Memberships', 'fedoracommunity.people/memberships',
                      params={'username':None}),
            MokshaApp('Package Maintenance', 'fedoracommunity.people/packagemaint',
                      params={'username':None}),
           )

class PeopleBrowserDashboard(DashboardContainer):
    layout = [Category('left-content-col',
                       (MokshaApp('All People', 'fedoracommunity.people/table', auth=not_anonymous()),
                        MokshaWidget('Login to browse a list of Fedora Users', 'fedoracommunity.login', auth=Not(not_anonymous()))
                       )
                      )]
    template = 'mako:fedoracommunity.mokshaapps.peopleresource.templates.people_browser'

name_widget = NameTabbedNav('namepeoplenav')
people_browser_widget = PeopleBrowserDashboard('peoplebrowserdashboard')

class RootController(Controller):
    @expose('mako:moksha.templates.widget')
    def index(self, username=None):
        if username:
            return self.name(username)

        tmpl_context.widget = people_browser_widget
        return {'options':{}}

    @expose('mako:moksha.templates.widget')
    def name(self, username):
        tmpl_context.widget = name_widget
        return {'options':{'username': username}}