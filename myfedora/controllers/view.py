from myfedora.lib.base import BaseController

from tg import expose
from myfedora.lib.appbundle import AppBundle, show_app
import pylons

class ViewController(BaseController):
    def __init__(self):
        super(ViewController, self).__init__() 

    def _create_view_app(self, view):
        return pylons.g.views[view](None, width="100%", height="100%")

    def _init_context(self, view):
        view_app = self._create_view_app(view)

        # may be used later on for extentions
        app_bundle = AppBundle('view_content')
        app_bundle.add(view_app)
   
        pylons.tmpl_context.show_app = show_app

        return app_bundle

    def index(self, view, action, **kw):
        self._init_context(view)
        return dict(view=view, args=kw)

    @expose('myfedora.templates.view')
    def default(self, view, action, data_key=None, tool=None, *args, **kw):
        app_bundle = self._init_context(view)
        return dict(view_content=\
            app_bundle.serialize_apps(pylons.tmpl_context.w),
                view=view, data_key=data_key, tool=tool, 
                    remainder=args, extra_kwds=kw)
