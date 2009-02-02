from moksha.lib.base import BaseController
from tg import expose, tmpl_context, override_template, request
from fedoracommunity.widgets import LoginWidget



login_widget = LoginWidget('login_widget');

class RootController(BaseController):

    @expose()
    def index(self, view='home'):
        tmpl_context.widget = login_widget
         
        if (view == 'canvas'):
            override_template(self.index, 'mako:fedoracommunity.mokshaapps.login.templates.index_canvas')
        else: # view = home
            override_template(self.index, 'mako:fedoracommunity.mokshaapps.login.templates.index')
        
        return {'came_from': request.headers.get('REFERER', '/')}