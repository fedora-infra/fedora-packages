import logging
import pkg_resources

from pylons import config

from myfedora.config.app_cfg import base_config

log = logging.getLogger(__name__)

load_environment = base_config.make_load_environment()

def load_widget_entry_points(app):
    entry_point_string = 'myfedora.plugins.apps.%s.views' %  app.entry_name
    log.info("Loading widgets for app %s on entry point %s" % (app.entry_name,
                                                               entry_point_string))

    for widget_entry in pkg_resources.iter_entry_points(entry_point_string):
        app.register_view(widget_entry.name, widget_entry.load())

def load_resourceviews():
    log.info("Loading MyFedora resourceview apps")
    for view in pkg_resources.iter_entry_points('myfedora.plugins.resourceviews'):
        if not config['pylons.app_globals'].resourceviews.has_key(view.name):
            view_class = view.load()
            view_class.load_resources()

            config['pylons.app_globals'].resourceviews[view.name] = view_class
            log.info(view.name + " loaded")

def load_fas():
    '''Load an instance of the Fedora Account System object.

    Since we only use the system fas account, we can create a single fas
    account for everyone.
    '''
    log.info("Loading fas")
    from fedora.client import AccountSystem
    fas = AccountSystem(config['fas.url'], username=config['fas.username'],
            password=config['fas.password'])
    config['pylons.app_globals'].fas = fas

def load_apps():
    log.info("Loading MyFedora apps")
    for app_entry in pkg_resources.iter_entry_points('myfedora.plugins.apps'):
        if not config['pylons.app_globals'].apps.has_key(app_entry.name):
            app_class = app_entry.load()
            config['pylons.app_globals'].apps[app_entry.name] = app_class
            load_widget_entry_points(app_class)
            app_class.load_widgets()
