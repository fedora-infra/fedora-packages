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
from tg import expose, tmpl_context


from moksha.api.widgets import ContextAwareWidget, Grid
from moksha.api.widgets.containers import DashboardContainer
from moksha.lib.helpers import Category, MokshaApp
from tw.api import Widget, JSLink, js_function
from tg import config

orbited_host = config.get('orbited_host', 'localhost')
orbited_port = config.get('orbited_port', 9000)
if orbited_port:
    orbited_url = '%s:%s' % (orbited_host, orbited_port)
else:
    orbited_url = orbited_host

orbited_js = JSLink(link=orbited_url + '/static/Orbited.js')

kamaloka_protocol_js = JSLink(modname='fedoracommunity.mokshaapps.demos', 
                              filename='js/amqp.protocol.js', 
                              javascript=[orbited_js])
kamaloka_protocol_0_10_js = JSLink(modname='fedoracommunity.mokshaapps.demos', 
                              filename='js/amqp.protocol_0_10.js', 
                              javascript=[kamaloka_protocol_js])
kamaloka_qpid_js = JSLink(modname='fedoracommunity.mokshaapps.demos', 
                              filename='js/qpid_amqp.js', 
                              javascript=[kamaloka_protocol_0_10_js])

timeping_demo_app = MokshaApp('Timeping AMQP Demo', 'fedoracommunity.demos/timeping_demo',
                               content_id='timeping_demo',
                               params={'rows_per_page': 10,
                                       'show_title': True,
                                       'filters':{}
                                      })

class DemoContainer(DashboardContainer, ContextAwareWidget):
    layout = [Category('full_sized_demo_apps',
                       timeping_demo_app)
             ]

demo_container = DemoContainer('demo')

class TimepingGrid(Grid, ContextAwareWidget):
    template='mako:fedoracommunity.mokshaapps.demos.templates.timeping_grid'
    javascript=Grid.javascript + [kamaloka_qpid_js]
    params=['orbited_port', 'orbited_host']
    resource=None
    resource_path=None
    orbited_port=9000
    orbited_host='localhost'
    
timeping_demo_grid = TimepingGrid('timeping_grid')    

class RootController(Controller):

    @expose('mako:moksha.templates.widget')
    def index(self):
        options = {}

        tmpl_context.widget = demo_container
        return {'options':options}
        
    @expose('mako:moksha.templates.widget')
    def timeping_demo(self, **kwds):
        options = {'orbited_port': orbited_port,
                   'orbited_host': orbited_host}
        tmpl_context.widget = timeping_demo_grid
        return {'options':options}
