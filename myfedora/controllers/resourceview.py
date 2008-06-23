from myfedora.lib.base import BaseController
import tg
from tg import expose
from myfedora.lib.appbundle import AppBundle
import pylons

class ResourceViewController(BaseController):
    def __init__(self):
        super(ResourceViewController, self).__init__() 

    def _create_view_app(self, resourceview, data_key, tool):
        return pylons.g.resourceviews[resourceview](None, 
                                                    width="100%", 
                                                    height="100%",
                                                    data_key=data_key,
                                                    tool=tool)

    def _init_context(self, view, data_key, tool):
        view_app = self._create_view_app(view, data_key, tool)

        # may be used later on for extentions
        app_bundle = AppBundle('view_content')
        app_bundle.add(view_app)
   
        return app_bundle

    def index(self, view, action, **kw):
        self._init_context(view)
        return dict(view=view, args=kw)

    @expose('myfedora.templates.view')
    def default(self, view, action, data_key=None, tool=None, *args, **kw):
        app_bundle = self._init_context(view, data_key=data_key, tool=tool)
        return dict(view_content=\
            app_bundle.serialize_apps(pylons.tmpl_context.w),
                view=view, remainder=args, extra_kwds=kw)

# alias for TG's controller loader
ResourceviewController = ResourceViewController
