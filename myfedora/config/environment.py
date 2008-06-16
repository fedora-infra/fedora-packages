"""Pylons environment configuration"""
import os
import pkg_resources

from tg import defaults
from pylons import config
from pylons.i18n import ugettext
from genshi.filters import Translator
from genshi.template import TemplateLoader
from sqlalchemy import engine_from_config

from fedora.accounts.fas2 import AccountSystem

import myfedora.lib.app_globals as app_globals
from myfedora.model import init_model, DBSession, metadata
#import myfedora.lib.helpers
#from myfedora.config.routing import make_map

def template_loaded(template):
    "Plug-in our i18n function to Genshi."
    template.filters.insert(0, Translator(ugettext))

def load_widgets():
    print "Loading Widgets"
    for widget_type in ('home', 'canvas', 'profile', 'config', 'preview'):
        our_widgets = config['pylons.app_globals'].widgets[widget_type]
        entry_point_string = 'myfedora.widgets.%s' % widget_type
        for widget in pkg_resources.iter_entry_points(entry_point_string):
            if not our_widgets.has_key(widget.name):
                our_widgets[widget.name] = widget.load()(widget.name)
                print our_widgets[widget.name]

def load_views():
    print "Loading MyFedora views"
    for view in pkg_resources.iter_entry_points('myfedora.plugins.views'):
        if not config['pylons.app_globals'].views.has_key(view.name):
            config['pylons.app_globals'].views[view.name] = view.load()()
            print config['pylons.app_globals'].views[view.name]

def load_fas():
    '''Load an instance of the Fedora Account System object.

    Since we only use the system fas account, we can create a single fas
    account for everyone.
    '''
    print "Loading fas"
    fas = AccountSystem(config['fas.url'], username=config['fas.username'],
            password=config['fas.password'])
    config['pylons.app_globals'].fas = fas

def load_apps():
    print "Loading MyFedora apps"
    for app in pkg_resources.iter_entry_points('myfedora.apps'):
        if not config['pylons.app_globals'].apps.has_key(app.name):
            config['pylons.app_globals'].apps[app.name] = app.load()
        print config['pylons.app_globals'].apps[app.name]

def load_environment(global_conf, app_conf):
    """Configure the Pylons environment via the ``pylons.config``
    object
    """
    # Pylons paths
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    paths = dict(root=root,
                 controllers=os.path.join(root, 'controllers'),
                 static_files=os.path.join(root, 'public'),
                 templates=[os.path.join(root, 'templates')])

    # Initialize config with the basic options
    config.init_app(global_conf, app_conf, package='myfedora', paths=paths)

    # This setups up a set of default route that enables a standard
    # TG2 style object dispatch.   Fell free to overide it with
    # custom routes.  TODO: Link to TG2+routes doc.
    make_map = defaults.make_default_route_map

    config['routes.map'] = make_map()
    config['pylons.app_globals'] = app_globals.Globals()
    #config['pylons.h'] = myfedora.lib.helpers

    # Load widgets from the myfedora.widgets entry point
    load_widgets()

    # Load myfedora's View/Tool infrastructure
    load_views()

    # Load all "Applications" from the myfedora.apps entry point
    load_apps()

    # Start our DataStreamer thread
    config['pylons.app_globals'].datastreamer.start()

    # Create the Genshi TemplateLoader
    config['pylons.app_globals'].genshi_loader = TemplateLoader(
        paths['templates'], auto_reload=True)

    # If you'd like to change the default template engine used to render
    # text/html content, edit these options.
    default_template_engine = 'genshi'
    default_template_engine_options = {}
    config['buffet.template_engines'].pop()
    config.add_template_engine(default_template_engine, '${package}.templates',
                               default_template_engine_options)

    # Setup SQLAlchemy database engine
    engine = engine_from_config(config, 'sqlalchemy.')
    config['pylons.app_globals'].sa_engine = engine

    # Pass the engine to initmodel, to be able to introspect tables
    init_model(engine)
    DBSession.configure(bind=engine)
    metadata.bind = engine

    # CONFIGURATION OPTIONS HERE (note: all config options will override
    # any Pylons config options)
