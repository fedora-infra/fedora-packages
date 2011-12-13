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

from fedoracommunity.lib import app_globals
import fedoracommunity
import fedoracommunity.lib

from tg.configuration import AppConfig, Bunch
from paste.deploy.converters import asbool
from pylons.i18n import ugettext

class FedoraCommunityConfig(AppConfig):
    tw2_initialize = False

    def add_tosca2_middleware(self, app):
        if self.tw2_initialize:
            return app

        from tg import config
        from tw2.core.middleware import Config, TwMiddleware
        default_tw2_config = dict( default_engine=self.default_renderer,
                                   translator=ugettext,
                                   auto_reload_templates=asbool(self.get('templating.mako.reloadfromdisk', 'false'))
                                   )
        res_prefix = config.get('fedoracommunity.resource_path_prefix')
        if res_prefix:
            default_tw2_config['res_prefix'] = res_prefix
        if getattr(self, 'custon_tw2_config', None):
            default_tw2_config.update(self.custom_tw2_config)
        app = TwMiddleware(app, **default_tw2_config)
        self.tw2_initialized = True
        return app

#    def add_auth_middleware(self, app, *args):
#        """ Add our FAS authentication middleware """
#        from fedoracommunity.connectors.faswhoplugin import fas_make_who_middleware
#        #from repoze.what.plugins.pylonshq import booleanize_predicates
#        from copy import copy
#        import logging
#
#        # TODO: go through moksha.lib.helpers and clean up the Predicate usage.
#        # Eventually we want to be using this, because this is how TG2/Pylons
#        # does it, however it currently breaks things for us...
#        #booleanize_predicates()
#
#        # Configuring auth logging:
#        if 'log_stream' not in self.fas_auth:
#            self.fas_auth['log_stream'] = logging.getLogger('auth')
#
#        auth_args = copy(self.fas_auth)
#
#        app = fas_make_who_middleware(app, **auth_args)
#        return app


base_config = FedoraCommunityConfig()
#base_config = AppConfig()
base_config.renderers = []
base_config.use_dotted_templatenames = True

base_config.use_toscawidgets = False
base_config.use_toscawidgets2 = True

base_config.package = fedoracommunity

# Set the default renderer
base_config.default_renderer = 'mako'
base_config.renderers.append('mako')
base_config.renderers.append('genshi')
base_config.auto_reload_templates = True
base_config.use_legacy_renderer = False

# Configure the base SQLALchemy Setup
base_config.use_sqlalchemy = False # fix this later
# base_config.model = myfedora.model
# base_config.DBSession = myfedora.model.DBSession

# Configure the authentication backend

# Setting this to 'sqlalchemy' ensures that our
# FedoraCommunityConfig.add_auth_middleware will get called.
# This is very broken in the code
#base_config.auth_backend = 'sqlalchemy'
#base_config.fas_auth = Bunch()

#base_config.sa_auth = Bunch()
#base_config.sa_auth.dbsession = model.DBSession
#base_config.sa_auth.user_class = model.User
#base_config.sa_auth.group_class = model.Group
#base_config.sa_auth.permission_class = model.Permission
#base_config.sa_auth.user_criterion = model.User.user_name
#base_config.sa_auth.user_id_column = 'user_id'

# override this if you would like to provide a different who plugin for.
# managing login and logout of your application
#base_config.sa_auth.form_plugin = None

# Enable profiling middleware.
base_config.profile = False

# Enable squeeze middlware
base_config.squeeze = False
