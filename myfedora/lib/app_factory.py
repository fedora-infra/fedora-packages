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
#            John Palmieri <johnp@redhat.com>
#            Toshio Kuratomi <tkuratom@redhat.com>

import pylons
import pkg_resources
from myfedora.widgets.resourceview import ResourceViewWidget
from myfedora.lib.utils import pretty_print_map

### FIXME: Write this so saving works.
#from fedora.client import ProxyClient

class AppFactory(object):
    '''
    An ``AppFactory`` is created per page load for each widget.  It associates
    a widget with the data that the widget needs to render.  It is also
    responsible for retrieving the data.  The widget is usually precreated and
    the ``AppFactory`` merely forms the association.

    :Class-property:
        :entry_name: When subclassing AppFactory this class property must be
            set to the setup.py base entrypoint for this app
        :display_name:When subclassing AppFactory this class property should be
            set to a text string which can be displayed to reference this app
        :view_widgets: This is set as widgets are registered 
    '''
    _user_fas = None

    entry_name = '' # Subclasses must set this
    display_name = '' # Subclass should set this
    
    _view_widgets = {}

    def __init__(self, app_config_id, width=None, height=None, view='home', **kw):
        '''Create an ``AppFactory``.
        
        :Parameters:
            :app_config_id: key for looking up configuration data if
                the user is logged in

        :Keyword Parameters:
            :width: width to display the app in (default = None)
            :height: height to display the app in (default = None)
            :view: the view to render this app as (default = 'home')
                * Home - the app should display as if on a home page 
                * Canvas - the app should display as if it has the full browser
                    window
                * Profile - the app should display as if the user is looking 
                    at their profile
                * Preview - the app should display random data
                * Config - the app should display it's configuration UI
            :kw: arbitrary configuration info for the app 
        '''
        if not self.entry_name:
            raise NotYetImplementedError, 'class variable entry_name must be set before this class can be instantiated'
        self.config_id = app_config_id
        self.width = width
        self.height = height 
        self.data = kw
        self.view = view.lower()
        self.data['config'] = {}
 
### FIXME: make ProxyClient work and then this can be used for saving configs
#    def _get_auth_fas(self):
#        if not self._user_fas:
#            self.userFas = ProxyClient(config['pylons.app_globals'].fas,
#                    useragent='MyFedora ProxyClient/0.1')
#        return self._user_fas

    def load_configs(self, force_refresh=False):
        '''Load a config from the FAS db into MyFedora.

        This method does not currently cache the configs but may in the future.

        Keyword Arguments:
        :force_refresh: If True, reload the config regardless of any
            caching
        '''
        #if tmpl_context.identity.current.anonymous:
        #    ### FIXME: Define the default_config
        #    return self.__default_config

        #fas = config['pylons.app_globals'].fas

        # set defaults
        configs = dict(config_id = self.config_id,
                       width = self.width, 
                       height = self.height)
        ### FIXME: fedora.accounts.fas2.AccountSystem method needed

        #configs.update(fas.get_configs_like(tmpl_context.identity.current.username, 'myfedora',
        #        self.config_id))

        return configs

    def save_configs(self, configs):
        '''Save the configuration of the widget into the FAS db.
        '''
        pass
        ### FIXME: Saving won't work until we can get a ProxyClient-fas that
        # performs actions on behalf of the user.
        #fas = self._get_auth_fas()
        #fas.set_configs(configs)

    def del_configs(self, configs):
        '''Remove a config from fas.'''
        pass
        ### FIXME: Saving won't work until we can get a ProxyClient-fas that
        # performs actions on behalf of the user.
        #fas = self._get_auth_fas()
        #fas.del_configs(configs)

    def get_data(self, force_refresh=False):
        '''Retrieve data necessary to render the widget.

        Keyword Arguments:
        :force_refresh: One day we'll implement caching.  This makes us
            disregard that when fetching data.
        '''
        data = dict(**self.data)
        
        data['config'].update(self.load_configs())
        data['name'] = self.entry_name
        # If there's data other than configs from fas, get it here.
        return data
    
    @staticmethod
    def __get_namespace(cls):
        ns_view = "%s.%s" % (cls.__module__, cls.__name__)
        return ns_view
         
    @classmethod
    def register_view(cls, view, view_cls):
        ns = cls.__get_namespace(cls)
        view_widgets = cls._view_widgets.get(ns, {})
        view_widgets[view] = view_cls
        cls._view_widgets[ns] = view_widgets

    @classmethod
    def load_widgets(cls):
        '''Register a widgets on a view if they haven't been already
        '''
        widgets = pylons.config['pylons.app_globals'].widgets
        ns = cls.__get_namespace(cls)
        for view, wcls in cls._view_widgets[ns].iteritems():
            if not widgets.has_key(wcls):
                name = cls.__get_namespace(wcls)
                widgets[wcls] = wcls(name)

    def get_widget(self, view = None):
        '''Returns the widget that renders this in that a specific view.
        '''
        
        if not view:
            view = self.view
            
        try:
            ns = self.__get_namespace(self.__class__)
            wcls = self._view_widgets[ns][view]
            w = pylons.config['pylons.app_globals'].widgets[wcls]
            widget_id = w.id
            self.data['config'].update({'widget_id': widget_id})

            return w
        except KeyError:
            ### FIXME: Raise a proper exception
            raise Exception, 'Unknown view type %s' % self.view

class ResourceViewAppFactory(AppFactory):
    _widget = None
    controller = None # this must be set by the child class

    def __init__(self, app_config_id, width=None, height=None, view='canvas', 
                data_key=None, tool=None, **kw):
        
        if not self.controller:
            raise NotYetImplementedError, 'class variable controller must be set before this class can be instantiated'
        
        super(ResourceViewAppFactory, self).__init__(app_config_id, 
            width, height, view, data_key=data_key, tool=tool, **kw)

        self.data_key = data_key
        self.tool = tool
        
    def get_widget(self, view=None):
        if not view:
            view = self.view
        
        widget_id = self._widget.id
        self.data['config'].update({'widget_id': widget_id})

        data_key = self.data['data_key']

        for c in self._widget.children:
            self.data.update({'child_args': {'data_key': data_key}})

        return self._widget

    # fixme, perhaps we should align this to the parent class by putting the 
    # widgets in the global namespace but this works fine
    @classmethod
    def load_widgets(cls):
        cls.tools_entry_point = "myfedora.plugins.resourceviews." + cls.entry_name + ".tools"

        child_tools = []
        for tool in pkg_resources.iter_entry_points(cls.tools_entry_point):
            child_tools.append(tool.load()(tool.name))
            
        cls._widget = ResourceViewWidget(cls.entry_name + '_view', children=child_tools)
        print "ReosurceView widget " + cls._widget.id + " loaded"

    @classmethod
    def load_controller(cls):
        cls.controller = cls.controller(cls)
        
    @classmethod
    def load_resources(cls):
        cls.load_controller()
        cls.load_widgets()