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

# The fedoracommunity moksha app root controller is our root controller

import pylons

from tg import expose, tmpl_context, redirect, flash, url, request, override_template

import moksha
from moksha.lib.base import BaseController

from fedoracommunity.widgets.search import XapianSearchGrid
from fedoracommunity.widgets.package import PackageWidget

class RootController(BaseController):

    @expose('mako:fedoracommunity.templates.error')
    def error(self, *args, **kw):
        resp = request.environ.get('pylons.original_response')
        return dict(prefix=request.environ.get('SCRIPT_NAME', ''),
                    code=str(request.params.get('code', resp.status_int)),
                    message=request.params.get('message', resp.body))

    @expose('mako:fedoracommunity.templates.search')
    def index(self, ec = None, **kwds):
        '''We show search page by default'''
        return self.s(**kwds)

    @expose('mako:fedoracommunity.templates.search')
    def s(self, *args, **kwds):
        '''Search controller'''
        search_str = ''

        if len(args) > 0:
            search_str = args[0]
        else:
            search_str = kwds.get('search', '')

        tmpl_context.widget = XapianSearchGrid
        return {'title': 'Fedora Packages Search',
                'options': {'id':'search_grid',
                            'filters':{'search':search_str}}
               }

    @expose('mako:fedoracommunity.widgets.templates.widget_loader')
    def _w(self, widget_name, *args, **kwds):
        '''generic widget controller - loads a widget from our widget list
           for dynamic loading of sections of the current page'''
        return {'widget': moksha.utils.get_widget(widget_name),
                'args': list(args), 'kwds': kwds}

    @expose()
    def _heartbeat(self, *args, **kwds):
        '''Fast heartbeat monitor so proxy servers know if we are runnining'''
        # TODO: perhaps we want to monitor our own internal functions and
        #       send back an error if we are not completely up and running
        return "Still running"

    @expose('mako:fedoracommunity.templates.chrome')
    def _default(self, *args, **kwds):
        '''for anything which does not hit a controller we assume is a package
           name'''
        package = args[0]
        tmpl_context.widget = PackageWidget
        return {'title': 'Package %s' % package, 'options':{'args': list(args), 'kwds': kwds}}

    # For older versions of TG2
    default = _default
