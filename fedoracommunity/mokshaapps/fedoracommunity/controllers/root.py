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

import pylons

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

        return {'title': 'Login - Fedora Community',
                'came_from': came_from,
                'options':{'came_from': came_from}}

    @expose('mako:fedoracommunity.mokshaapps.fedoracommunity.templates.invalid_path')
    def invalid_path(self, invalid_path):
        title = 'Invalid Path'
        split_path = invalid_path.split('/')
        first_path = None
        login = False
        for path in split_path:
            if path:
                first_path = path
                break

        # hack for now to see if we need to show a login box
        if first_path == 'my_profile':
            login = True
            title = 'Restricted Page'
            tmpl_context.widget = login_widget

        return {'title': title,
                'invalid_path': invalid_path,
                'login': login}

    @expose('mako:fedoracommunity.mokshaapps.fedoracommunity.templates.index')
    def _default(self, *args, **kwds):
        identity = request.environ.get('repoze.who.identity')
        if identity:
            csrf = identity.get('_csrf_token')
            if csrf:
                kwds['_csrf_token'] = csrf

        anchor='/'.join(args)
        if anchor:
            kwds['anchor'] = anchor

        url = pylons.url('/', **kwds)
        if url.startswith('/community'):
            url = url[10:]

        redirect(url)
