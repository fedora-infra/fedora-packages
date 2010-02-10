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

from moksha.api.widgets.containers import TabbedContainer
from moksha.api.widgets.containers.dashboardcontainer import applist_widget
from moksha.lib.helpers import Category

class ExtraContentTabbedContainer(TabbedContainer):
    params = ['applist_widget', 'sidebar_apps', 'header_apps']
    applist_widget = applist_widget
    sidebar_apps = []
    header_apps = []

    def update_params(self, d):
        d['sidebar_apps'] = Category('sidebar-apps', self.sidebar_apps).process(d)
        d['header_apps'] = Category('header-apps', self.header_apps).process(d)

        super(ExtraContentTabbedContainer, self).update_params(d)

class SubTabbedContainer(TabbedContainer):
    template = 'mako:fedoracommunity.widgets.templates.subtabbedcontainer'
    passPathRemainder = True