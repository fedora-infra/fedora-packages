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
from tg import expose, tmpl_context, override_template, request, url
from fedoracommunity.widgets import LoginWidget
from urlparse import urlparse

login_widget = LoginWidget('login_widget')

class RootController(Controller):

    @expose()
    def index(self, view='home', came_from=None):
        tmpl_context.widget = login_widget

        if (view == 'canvas'):
            override_template(self.index, 'mako:fedoracommunity.mokshaapps.login.templates.index_canvas')
        else: # view = home
            override_template(self.index, 'mako:fedoracommunity.mokshaapps.login.templates.index')


        if not came_from:
            came_from = url('/')
        else:
            # only redirect to relative addresses to avoid phishing
            purl = urlparse(came_from)
            came_from = purl.path
            if purl.query:
                came_from += '?' + purl.query

        return {'came_from': came_from}