from myfedora.lib.base import BaseController
from tg import expose, redirect
from myfedora.lib.appbundle import AppBundle
import pylons

class ResourceViewController(BaseController):
    def __init__(self, app_class):
        super(ResourceViewController, self).__init__() 
        self.app_class = app_class

    def _create_view_app(self, data_key, tool, **kw):
        return self.app_class(None, 
                              width="100%", 
                              height="100%",
                              data_key=data_key,
                              tool=tool,
                              **kw)

    def _init_context(self, data_key, tool, **kw):
        view_app = self._create_view_app(data_key, tool, **kw)

        if not view_app:
            return None
        
        # may be used later on for extensions
        app_bundle = AppBundle('view_content')
        app_bundle.add(view_app)
   
        return app_bundle

    def index(self, **kw):
        tool = kw.pop('tool', None)
        data_key = kw.pop('data_key', None)
        app_bundle = self._init_context(data_key, tool, **kw)
        data = app_bundle.serialize_apps(pylons.tmpl_context.w)
        result = {}
        result.update(kw)
        result.update(dict(view_content = data,
                           view = None))
        return result
        
    @expose('genshi:myfedora.templates.resourceviewcontainer')
    def default(self, view=None, view_action=None, data_key=None, tool=None, *args, **kw):
        if not view:
            view = self.app_class.entry_name
            
        pylons.tmpl_context.resource_view = view
            
        if view_action != 'name': 
            tool = view_action
            
        app_bundle = self._init_context(data_key=data_key, tool=tool, **kw)
        
        data = app_bundle.serialize_apps(pylons.tmpl_context.w)
        return dict(view_content = data,
                    view = view, 
                    remainder = args, 
                    extra_kwds = kw)