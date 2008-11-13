from myfedora.lib.base import BaseController
from tg import expose, redirect, url, flash
from myfedora.lib.appbundle import AppBundle
from myfedora.lib.exception import App404Error,AppRequiresAuth 
from myfedora.widgets.resourceview import DummyToolWidget
import pylons

class ResourceViewController(BaseController):
    def __init__(self, app_class):
        super(ResourceViewController, self).__init__() 
        self.app_class = app_class

    def _create_view_app(self, data_key, tool, **kw):
        print self.app_class
        if self.app_class.requires_auth:
            if (not pylons.tmpl_context.identity 
                or not pylons.tmpl_context.identity.get('person')):
                  raise AppRequiresAuth
            
        return self.app_class(None, 
                              width="100%", 
                              height="100%",
                              data_key=data_key,
                              tool=tool,
                              **kw)

    def _init_context(self, data_key, tool, **kw):
        view_app = self._create_view_app(data_key, tool, **kw)


        if not view_app:
            raise App404Error
        
        # may be used later on for extensions
        app_bundle = AppBundle('view_content')
        app_bundle.add(view_app)
   
        return app_bundle

    def index(self, **kw):
        # this is ugly, figure out how to support a different index page
        app = self.app_class
        child_widgets = app._widget.children
        
        ov = DummyToolWidget('overview', 'Overview')
        visible_children = [ov]
        childurls = {ov._id: '/%s/' % app.entry_name}
        for c in child_widgets:
            if c.requires_data_key:
                continue
            
            visible_children.append(c)
            
            path = pylons.request.environ['PATH_INFO']
            path_elements = path.split('/')
            path_count = len(path_elements) - path_elements.count('')
            childurls[c._id] = url("/%s/%s" % (app.entry_name,
                                   c._id)
                                  )
        
        return dict(visible_children=visible_children,
                    active_child=ov,
                    childurls=childurls)
        
    @expose('genshi:myfedora.templates.resourceviewcontainer')
    def default(self, view=None, view_action=None, data_key=None, tool=None, *args, **kw):
        if not view:
            view = self.app_class.entry_name
            
        pylons.tmpl_context.resource_view = view
            
        if view_action != 'name': 
            tool = view_action
            
        try:
            app_bundle = self._init_context(data_key=data_key, tool=tool, **kw)
        except App404Error, e:
            log.error(e)
            return pylons.Response(code=404)
        except AppRequiresAuth, e:
            flash('You are not authorized to access the page you requested')
            redirect(url('/login'))
            
        data = app_bundle.serialize_apps(pylons.tmpl_context.w)
        return dict(view_content = data,
                    view = view, 
                    remainder = args, 
                    extra_kwds = kw)