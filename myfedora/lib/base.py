"""The base Controller API

Provides the BaseController class for subclassing.
"""
from tg import TGController, tmpl_context, flash
from pylons.templating import render_genshi as render

from pylons import tmpl_context, request
import pylons
import myfedora.model as model

from pylons.i18n import _, ungettext, N_
from tw.api import WidgetBunch

from myfedora.lib.appbundle import AppBundle
from myfedora.widgets import GlobalResourceInjectionWidget

global_resource_injection = GlobalResourceInjectionWidget()

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
        global_resource_injection.register_resources()
        tmpl_context.identity =  request.environ.get('repoze.who.identity')
        
        auth_error = request.environ.get('FAS_AUTH_ERROR')
        if auth_error:
            flash(auth_error)

        #this can be overwritten by the child controller
        nav = pylons.g.apps['navigation'](None, '320px', '200px', 'Home')
        apps = AppBundle('sidebarapps')
        apps.add(nav)
        tmpl_context.sidebar_apps = apps.serialize_apps(pylons.tmpl_context.w)

        return TGController.__call__(self, environ, start_response)

class SecureController(BaseController):
    """this is a SecureController implementation for the
    tg.ext.repoze.who plugin.
    it will permit to protect whole controllers with a single predicate
    placed at the controller level.
    The only thing you need to have is a 'require' attribute which must
    be a callable. This callable will only be authorized to return True
    if the user is allowed and False otherwise. This may change to convey info
    when securecontroller is fully debugged...
    """

    def check_security(self):
        errors = []
        environ = request.environ
        identity = environ.get('repoze.who.identity')
        if not hasattr(self, "require") or \
            self.require is None or \
            self.require.eval_with_object(identity, errors):
            return True

        # if we did not return this is an error :)
        # TODO: do something with the errors variable like informing our user...
        return False
