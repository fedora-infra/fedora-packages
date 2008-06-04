"""Pylons environment configuration"""
import os
import pkg_resources

from tg import defaults
from pylons import config
from pylons.i18n import ugettext
from genshi.filters import Translator
from genshi.template import TemplateLoader
from sqlalchemy import engine_from_config

import myfedora.lib.app_globals as app_globals
from myfedora.model import init_model, DBSession, metadata
#import myfedora.lib.helpers
#from myfedora.config.routing import make_map

def template_loaded(template):
    "Plug-in our i18n function to Genshi."
    template.filters.insert(0, Translator(ugettext))

def load_widgets(widgets):
    print "Loading Widgets"
    for widget in pkg_resources.iter_entry_points('myfedora.widgets'):
        if not widgets.has_key(widget.name):
            widgets[widget.name] = widget.load()()
            print widgets[widget.name]

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
    load_widgets(config['pylons.app_globals'].widgets)

    # Start our DataStreamer thread
    config['pylons.app_globals'].datastreamer.start()

    # Create the Genshi TemplateLoader
    config['pylons.app_globals'].genshi_loader = TemplateLoader(
        search_path=paths['templates'], auto_reload=True)

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
