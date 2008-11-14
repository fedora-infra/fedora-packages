import logging
import pkg_resources

from routes import Mapper
from tg.configuration import AppConfig, Bunch, config

import myfedora
from myfedora import model
from myfedora.lib import app_globals, helpers

log = logging.getLogger(__name__)

class MyFedoraConfig(AppConfig):

    def setup_routes(self):
        """ Setup our custom routes """
        map = Mapper(directory=config['pylons.paths']['controllers'],
                     always_scan=config['debug'])

        # Setup a default route for the error controller
        map.connect('error/:action/:id', controller='error')
        for vname in config['pylons.app_globals'].resourceviews.keys():
            map.connect('/' + vname,
                        controller='resourcelocator',
                        action='lookup')
            map.connect('/' + vname + '/*url',
                        controller='resourcelocator',
                        action='lookup')

        # This route connects your root controller
        map.connect('*url', controller='root', action='routes_placeholder')

        config['routes.map'] = map

    def add_auth_middleware(self, app):
        """ Add our FAS authentication middleware """
        from myfedora.lib.faswhoplugin import fas_make_who_middleware
        app = fas_make_who_middleware(app, config)
        return app

    def make_load_environment(self):
        """ Returns a load_environment function """

        def load_environment(global_conf, app_conf):
            global_conf = Bunch(global_conf)
            app_conf = Bunch(app_conf)
            self.setup_paths()
            self.init_config(global_conf, app_conf)
            self.setup_helpers_and_globals()

            # Load myfedora's Applications, ResourceViews and Tools
            self.load_resourceviews()
            self.load_apps()

            self.setup_routes()

            if 'genshi' in self.renderers:
                self.setup_genshi_renderer()
            if 'mako' in self.renderers:
                self.setup_mako_renderer()
            if 'jinja' in self.renderers:
                self.setup_jinja_renderer()
            if self.use_legacy_renderer:
                self.setup_default_renderer()
            if self.use_sqlalchemy:
                self.setup_sqlalchemy()

        return load_environment

    def load_widget_entry_points(self, app):
        entry_point_string = 'myfedora.plugins.apps.%s.views' %  app.entry_name
        log.info("Loading widgets for app %s on entry point %s" % (
                 app.entry_name, entry_point_string))
        for widget_entry in pkg_resources.iter_entry_points(entry_point_string):
            app.register_view(widget_entry.name, widget_entry.load())

    def load_resourceviews(self):
        log.info("Loading MyFedora resourceview apps")
        for view in pkg_resources.iter_entry_points('myfedora.plugins.resourceviews'):
            if not config['pylons.app_globals'].resourceviews.has_key(view.name):
                view_class = view.load()
                view_class.load_resources()

            config['pylons.app_globals'].resourceviews[view.name] = view_class
            log.info(view.name + " loaded")

    def load_fas(self):
        '''Load an instance of the Fedora Account System object.

        Since we only use the system fas account, we can create a single fas
        account for everyone.
        '''
        log.info("Loading fas")
        from fedora.client import AccountSystem
        fas = AccountSystem(config['fas.url'], username=config['fas.username'],
                password=config['fas.password'])
        config['pylons.app_globals'].fas = fas

    def load_apps(self):
        log.info("Loading MyFedora apps")
        for app_entry in pkg_resources.iter_entry_points('myfedora.plugins.apps'):
            if not config['pylons.app_globals'].apps.has_key(app_entry.name):
                app_class = app_entry.load()
                config['pylons.app_globals'].apps[app_entry.name] = app_class
                self.load_widget_entry_points(app_class)
                app_class.load_widgets()


base_config = MyFedoraConfig()
base_config.renderers = []

base_config.package = myfedora

# Set the default renderer
base_config.default_renderer = 'genshi'
base_config.renderers.append('genshi')
base_config.renderers.append('mako')
base_config.auto_reload_templates = True

# Configure the base SQLALchemy Setup
base_config.use_sqlalchemy = True
base_config.model = myfedora.model
base_config.DBSession = myfedora.model.DBSession

# Configure the authentication backend

# Setting this to 'sqlalchemy' ensures that our
# MyFedoraConfig.add_auth_middleware will get called.
base_config.auth_backend = 'sqlalchemy'

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
