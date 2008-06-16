from myfedora.lib.base import Controller
from myfedora.lib.appbundle import AppBundle, show_app
from tg import expose
import pylons

class AppController(Controller):
    """AppController provide the base controller for serving applications"""

    @expose('myfedora.templates.apps')    
    def name(self, app_id, app_config_id=None, width=None, height=None, 
                view='Home', **kw):
        """
        Handle a request for an app and pass the keywords hash
        
        :Parameters:
            :app_id: the name of the app to load
            :app_config_id: key for looking up configuration data if
                the user is logged in
            :width: width to display the app in ()
            :height: height to display the app in
            :view: view to show the app in can be show in
                * Home - the app should display as if on a home page 
                * Canvas - the app should display as if it has the full browser
                  window
                * Profile - the app should display as if the user is looking 
                  at their profile
                * Preview - the app should display random data
                * Config - the app should display it's configuration UI
            :kw: list of paramaters to send to the app
            
        :Exceptions:
            :LookupError: raised if we cannot find the app
        """
        app_bundle = AppBundle('standalone')
        appclass = self._find_app(app_id)
        app = appclass(app_config_id, width, height, view, **kw)
        app_bundle.add(app)

        pylons.tmpl_context.show_app = show_app

        return dict(standalone_data = app_bundle.serialize_apps(pylons.tmpl_context.w))
   
    @expose() 
    def list(self):
        # quick list for now
        result = "<ul>"
        for key in pylons.g.apps.keys():
            result += "<li><a href='name/%s'>%s</a></li>" % (key, key)
        
        return result 
                        
    def _find_app(self, app_id):
        """Find the app class in globals
        
        :Parameters:
            :app_id: the id of the app we are looking for
        
        :Exceptions:
            :LookupError: raised if we cannot find the app
        """
        try:
            appclass = pylons.g.apps[app_id]
        except:
            raise LookupError("App %s is not registered with MyFedora" % app_id)
            
        return appclass
