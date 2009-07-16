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

from tg import expose, tmpl_context
from moksha.lib.base import Controller
from moksha.lib.helpers import Category, MokshaApp
from moksha.api.widgets.containers.dashboardcontainer import applist_widget

from fedoracommunity.widgets import SubTabbedContainer
from fedoracommunity.mokshaapps.statistics.widgets import wiki_stats_dashboard
#from fedoracommunity.mokshaapps.statistics.widgets import updates_stats_dashboard

class StatsNavContainer(SubTabbedContainer):
    params = ['applist_widget']
    applist_widget = applist_widget
    template='mako:fedoracommunity.mokshaapps.statistics.templates.stats_nav'
    tabs = (
        Category('Applications', (
            MokshaApp('Wiki', 'fedoracommunity.statistics/wiki', params={}),
            #MokshaApp('Updates', 'fedoracommunity.statistics/updates', params={}),
            ),
        ),
    )

statistics_nav_container = StatsNavContainer('statistics_nav_container')


class RootController(Controller):

    @expose('mako:moksha.templates.widget')
    def index(self):
        tmpl_context.widget = statistics_nav_container
        return dict(options={})

    @expose('mako:moksha.templates.widget')
    def wiki(self):
        tmpl_context.widget = wiki_stats_dashboard
        return dict(options={})

    #@expose('mako:moksha.templates.widget')
    #def updates(self):
    #    tmpl_context.widget = updates_stats_dashboard
    #    return dict(options={})
