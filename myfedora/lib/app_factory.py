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

from tg import identity
# Is this right for tg2?
# from TemplateContext import identity
from pylons import config
### FIXME: Write this so saving works.
#from fedora.client import ProxyClient

class AppFactory(object):
    '''
    An ``AppFactory`` is created per page load for each widget.  It associates
    a widget with the data that the widget needs to render.  It is also
    responsible for retrieving the data.  The widget is usually precreated and
    the ``AppFactory`` merely forms the association.
    '''
    _user_fas = None

    entry_name = '' # Subclasses must set this

    def __init__(app_config_id, width=None, height=None):
        '''Create an ``AppFactory``.
        
        :Parameters:
            :app_config_id: key for looking up configuration data if
                the user is logged in

        :Keyword Parameters:
            :width: width to display the app in (None = default)
            :height: height to display the app in (None = default)
        '''
        if not entry_name:
            raise NotYetImplementedError, 'class variable entry_name must be set before this class can be instantiated'
        self.config_id = app_config_id
        self.width = width
        self.height = height
 
### FIXME: make ProxyClient work and then this can be used for saving configs
#    def _get_auth_fas(self):
#        if not self._user_fas:
#            self.userFas = ProxyClient(config['pylons.app_globals'].fas,
#                    useragent='MyFedora ProxyClient/0.1')
#        return self._user_fas

    def load_config(self, force_refresh=False):
        '''Load a config from the FAS db into MyFedora.

        This method does not currently cache the configs but may in the future.

        Keyword Arguments:
        :force_refresh: If True, reload the config regardless of any
            caching
        '''
        if identity.current.anonymous:
            ### FIXME: Define the default_config
            return self.__default_config

        fas = config['pylons.app_globals'].fas

        ### FIXME: fedora.accounts.fas2.AccountSystem method needed
        configs = fas.get_configs_like(identity.current.username, 'myfedora',
                self.app_config_id)
        
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

    config = property(load_config, save_config, del_config,
                      'Config information for this AppFactory')

    def get_data(self, force_refresh=False):
        '''Retrieve data necessary to render the widget.

        Keyword Arguments:
        :force_refresh: One day we'll implement caching.  This makes us
            disregard that when fetching data.
        '''
        data = dict(config=self.config)
        # If there's data other than configs from fas, get it here.
        return data

    def get_widget(view='home'):
        '''Returns the widget that renders this in that a specific view.

        Keyword Arguments:
        :view: view to show the app in can be show in
            * Home - the app should display as if on a home page 
            * Canvas - the app should display as if it has the full browser
                window
            * Profile - the app should display as if the user is looking 
                at their profile
            * Preview - the app should display random data
            * Config - the app should display it's configuration UI
        '''
        try:
            return config['pylons.app_globals'].widgets[view.lower()][ \
                    self.entry_name]
        except KeyError:
            ### FIXME: Raise a proper exception
            raise Exception, 'Unknown view type %s' % view
