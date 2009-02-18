from fedoracommunity.lib import app_globals, helpers
import fedoracommunity
import fedoracommunity.lib

from tg.configuration import AppConfig, Bunch

class FedoraCommunityConfig(AppConfig):
    def add_auth_middleware(self, app):
        """ Add our FAS authentication middleware """
        from fedoracommunity.connectors.faswhoplugin import fas_make_who_middleware
        from copy import copy
        import logging

        # Configuring auth logging:
        if 'log_stream' not in self.fas_auth:
            self.fas_auth['log_stream'] = logging.getLogger('auth')

        auth_args = copy(self.fas_auth)

        app = fas_make_who_middleware(app, **auth_args)
        return app

base_config = FedoraCommunityConfig()
base_config.renderers = []
base_config.use_dotted_templatenames = True

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
base_config.auth_backend = 'sqlalchemy'
base_config.fas_auth = Bunch()

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
