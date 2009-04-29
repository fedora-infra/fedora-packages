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

from tg import expose, tmpl_context, redirect, flash, url, request

from moksha.lib.base import BaseController
from moksha.api.widgets.containers import TabbedContainer
from moksha.api.errorcodes import login_err

from fedoracommunity.mokshaapps.login import login_widget

# Root for the whole fedora-community tree
class MainNav(TabbedContainer):
    template = 'mako:fedoracommunity.mokshaapps.fedoracommunity.templates.mainnav'
    config_key = 'fedoracommunity.mainnav.apps'
    staticLoadOnClick = True

class RootController(BaseController):

    def __init__(self):
        self.mainnav_tab_widget = MainNav('main_nav_tabs', action="create")

    @expose('mako:fedoracommunity.mokshaapps.fedoracommunity.templates.index')
    def index(self, ec = None, **kwds):
        # FIXME: we won't always display the main nav
        tmpl_context.widget = self.mainnav_tab_widget

        return {'title': 'Fedora Community', 'options':kwds}

    @expose('mako:fedoracommunity.mokshaapps.fedoracommunity.templates.login')
    def login(self, came_from = '/', ec = None):
        tmpl_context.widget = login_widget

        if ec:
            err = None
            try:
                err = login_err(ec)
            except AttributeError, e:
                pass

            if err:
                flash(err)

        if '/logout_handler' in came_from:
            came_from = url('/')

        return {'title': 'Fedora Community Login',
                'came_from': came_from,
                'options':{'came_from': came_from}}

    @expose('mako:fedoracommunity.mokshaapps.fedoracommunity.templates.index')
    def default(self, *args, **kwds):
        identity = request.environ.get('repoze.who.identity')
        if identity:
            csrf = identity.get('_csrf_token')
            if csrf:
                kwds['_csrf_token'] = csrf

        redirect('/', anchor='/'.join(args), params=kwds)
