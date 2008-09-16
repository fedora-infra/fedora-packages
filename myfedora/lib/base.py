"""The base Controller API

Provides the BaseController class for subclassing.
"""
from tg import TGController, tmpl_context
from pylons.templating import render_genshi as render

from pylons import tmpl_context, request
import pylons
import myfedora.model as model

from pylons.i18n import _, ungettext, N_
from tw.api import WidgetBunch

from myfedora.widgets import GlobalResourceInjectionWidget
from myfedora.lib.appbundle import AppBundle

def show_app(app):
    """Helper function for showing myfedora apps in a template
       This gets injected into the tmpl_context by the controller
    """ 
    params = request.params

    widget_id = app['config']['widget_id']
    uid = app['config']['uid']
    id_prefix = uid + "_"
    id_prefix_len = len(id_prefix)
    for k in params.iterkeys():
        if k.startswith(id_prefix):
            p = k[id_prefix_len:]
            if not app.has_key(p):
                app[p] = params[k]

    w = tmpl_context.w[widget_id]
    return w.display(id = uid, **app)

class Controller(object):
    """Base class for a web application's controller.
    
    Currently, this provides positional parameters functionality
    via a standard default method.
    """
    
class BaseController(TGController):
    """Base class for the root of a web application.
    
    Your web application should have one of these. The root of
    your application is used to compute URLs used by your app.
    """
    _global_resource_injection = GlobalResourceInjectionWidget()
    
    def __call__(self, environ, start_response):
        """Invoke the Controller"""
        # TGController.__call__ dispatches to the Controller method
        # the request is routed to. This routing information is
        # available in environ['pylons.routes_dict']

        # Create a container to send widgets to the template. Only those sent
        # in here will have their resources automatically included in the
        # template
        tmpl_context.w = WidgetBunch()
        tmpl_context.show_app = show_app
        tmpl_context.resource_view = ''
        self._global_resource_injection.register_resources()
        tmpl_context.identity =  pylons.request.environ.get('repoze.who.identity')
        
        #this can be overwritten by the child controller
        nav = pylons.g.apps['navigation'](None, '320px', '200px', 'Home')
        apps = AppBundle('sidebarapps')
        apps.add(nav)
        tmpl_context.sidebar_apps = apps.serialize_apps(pylons.tmpl_context.w)
        
        try:
            return TGController.__call__(self, environ, start_response)
        finally:
            #after everything is done clear out the Database Session
            #to eliminate possible cross request DBSession polution.
            model.DBSession.remove()
        
