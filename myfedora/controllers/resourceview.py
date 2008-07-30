from myfedora.lib.base import BaseController
from tg import expose, redirect
from myfedora.lib.appbundle import AppBundle
import pylons

class ResourceViewController(BaseController):
    def __init__(self, app_class):
        super(ResourceViewController, self).__init__() 
        self.app_class = app_class

    def _create_view_app(self, data_key, tool):
        return self.app_class(None, 
                              width="100%", 
                              height="100%",
                              data_key=data_key,
                              tool=tool)

    def _init_context(self, data_key, tool):
        view_app = self._create_view_app(data_key, tool)

        # may be used later on for extensions
        app_bundle = AppBundle('view_content')
        app_bundle.add(view_app)
   
        return app_bundle

    @expose()
    def index(self, view):
        app_bundle = self._init_context(None, None)
        data = app_bundle.serialize_apps(pylons.tmpl_context.w)
        return dict(view_content = data,
                    view = view)
        
    @expose('genshi:myfedora.templates.view')
    def default(self, view, view_action=None, data_key=None, tool=None, *args, **kw):
        if not view_action:
            return self.index(view)
        elif view_action != 'name': 
            tool = view_action
            
        app_bundle = self._init_context(data_key=data_key, tool=tool)
        data = app_bundle.serialize_apps(pylons.tmpl_context.w)
        return dict(view_content = data,
                    view = view, 
                    remainder = args, 
                    extra_kwds = kw)