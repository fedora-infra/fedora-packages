# Copyright (C) 2008  Red Hat, Inc. All rights reserved.
#
# This copyrighted material is made available to anyone wishing to use, modify,
# copy, or redistribute it subject to the terms and conditions of the GNU
# General Public License v.2.  This program is distributed in the hope that it
# will be useful, but WITHOUT ANY WARRANTY expressed or implied, including the
# implied warranties of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.  You should have
# received a copy of the GNU General Public License along with this program; if
# not, write to the Free Software Foundation, Inc., 51 Franklin Street, Fifth
# Floor, Boston, MA 02110-1301, USA. Any Red Hat trademarks that are
# incorporated in the source code or documentation are not subject to the GNU
# General Public License and may only be used or replicated with the express
# permission of Red Hat, Inc.
#
# Author(s): Luke Macken <lmacken@redhat.com>

import pylons
import logging

from tg import expose, flash
from tgrepozewho import authorize
from pylons.i18n import ugettext as _

#from tg import redirect, validate
#from myfedora.model import DBSession, metadata
#from dbsprockets.dbmechanic.frameworks.tg2 import DBMechanic
#from dbsprockets.saprovider import SAProvider

from myfedora.lib.base import BaseController

log = logging.Logger(__name__)

# How do we keep track of what widgets a user is looking at?
# - pull it from our WSGI environ!
#   meaning we need something to put it there (sessions?)

class RootController(BaseController):

    #admin = DBMechanic(SAProvider(metadata), '/admin')

    @expose()
    def join(self, feed, *args, **kw):
        print "join(%s, %s, %s)" % (feed, args, kw)
        if pylons.g.widgets.has_key(feed):
            pylons.g.datastreamer.join('bobvila', feed)
        else:
            log.error("Unknown data feed: %s" % feed)
        return ""

    @expose('myfedora.templates.index')
    def index(self):
        # Figure out what widgets we need to show
        # Add them to the pylons.tmpl_context.w
        # Get the data to populate them
        #  - from where ?
        #   Depending on the type of widget, maybe here, or maybe the widget
        #   is self-populating (comet, etc).
        #    Widgets need a data store!
        #      Since our widgets are stateless, and singletons,
        #      They can be self-populating/publishing?!
        # Pass data to template
        pylons.tmpl_context.w.people = pylons.g.widgets.values()[0]
        return dict(page='index')

    @expose('pluginname.templates.about')
    def about(self):
        return dict(page='about')

    @expose('myfedora.templates.about')
    @authorize.require(authorize.has_permission('manage'))
    def manage_permission_only(self, **kw):
        return dict(page='about')

    @expose('myfedora.templates.about')
    @authorize.require(authorize.is_user('editor'))
    def editor_user_only(self, **kw):
        return dict(page='about')

    @expose('myfedora.templates.login')
    def login(self, **kw):
        came_from = kw.get('came_from', '/')
        return dict(page='login', header=lambda *arg: None,
                    footer=lambda *arg: None, came_from=came_from)
