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
from pylons.i18n import ugettext as _

#from tg import redirect, validate
#from myfedora.model import DBSession, metadata
#from dbsprockets.dbmechanic.frameworks.tg2 import DBMechanic
#from dbsprockets.saprovider import SAProvider

from myfedora.lib.base import BaseController
from myfedora.lib.appbundle import AppBundle
from myfedora.controllers.apps import AppController
from myfedora.controllers.extensions import ExtensionsController
from myfedora.controllers.proxy import ProxyController
log = logging.Logger(__name__)

class RootController(BaseController):

    #admin = DBMechanic(SAProvider(metadata), '/admin')
    apps = AppController()
    extensions = ExtensionsController()
    proxy = ProxyController()
    
    @expose()
    def join(self, feed, *args, **kw):
        """ Join a specified data feed """
        print "join(%s, %s, %s)" % (feed, args, kw)
        # Right now the names of the data feed are the names of the widgets
        # themselves.  This needs to change.
        # We also need to handle streaming data to logged in and anonymous
        # users.
        if pylons.g.widgets.has_key(feed):
            pylons.g.datastreamer.join('bobvila', feed)
        else:
            log.error("Unknown data feed: %s" % feed)
        return ""

    @expose('myfedora.templates.index')
    def index(self):
        leftcol_apps = AppBundle("leftcol")
        rightcol_apps = AppBundle("rightcol")

        if not pylons.tmpl_context.identity:
            placeholder = pylons.g.apps['placeholder'](None, '285px', '272px', 'Canvas', placeholder_label='Fedora is Cool banner')
            leftcol_apps.add(placeholder)
            
            
            login = pylons.g.apps['login'](None, '320px', '200px', 'Home')
            rightcol_apps.add(login)
        
        placeholder = pylons.g.apps['placeholder'](None, '285px', '272px', 'Home', placeholder_label='Alerts Placeholder')
        rightcol_apps.add(placeholder)
        
        #url = "http://gmodules.com/ig/ifr?url=http://www.cammap.net/tvlive/livetvint.xml&amp;up_kanaal=BBC%20World&amp;up_autoplay=Yes&amp;up_none=-%20Fill%20in%20below%20-&amp;up_statn=&amp;up_urls=&amp;up_urlw=http%3A%2F%2F&amp;synd=open&amp;w=285&amp;h=272&amp;title=Live+TV+channels&amp;border=%23ffffff%7C3px%2C1px+solid+%23999999&amp;output=js"

        #planet_fedora = pylons.g.apps['planetfedora'](None, '285px', '272px', 'Canvas', url=url)
        #col2_apps.add(planet_fedora)
        
        


        rightcol_apps = rightcol_apps.serialize_apps(pylons.tmpl_context.w)
        leftcol_apps = leftcol_apps.serialize_apps(pylons.tmpl_context.w)

        return dict(page='index', leftcol_apps = leftcol_apps, 
                                  rightcol_apps = rightcol_apps)

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
        came_from = kw.get('came_from', 
                            pylons.request.headers.get('REFERER', '/'))
        return dict(page='login', header=lambda *arg: None,
                    footer=lambda *arg: None, came_from=came_from)
