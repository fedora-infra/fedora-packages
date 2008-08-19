from tw.api import Widget
from tw.jquery import jquery_js
from myfedora.lib.app_factory import AppFactory
from tg import url
from pylons import request

class LoginApp(AppFactory):
    entry_name = 'login'

class LoginWidget(Widget):
    params=['username', 'password']
    template = 'genshi:myfedora.apps.templates.login'
    javascript = [jquery_js]

    def update_params(self, d):
        super(LoginWidget, self).update_params(d)
        
        if not 'came_from' in d:
            d['came_from'] = request.environ.get('PATH_INFO')
        
        return d