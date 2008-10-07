from tw.api import Widget, js_function
from tw.jquery import JQuery,jquery_js
from myfedora.lib.app_factory import AppFactory
from myfedora.lib.proxy import PkgdbClient
from myfedora.lib.utils import odict
from myfedora.widgets.widgets import myfedora_extensions_js, myfedora_ui_js

from pylons import app_globals, request, tmpl_context
from tg import url

from urlparse import urlparse

class UserAlertsApp(AppFactory):
    entry_name = 'useralerts'
    
    def __init__(self, 
                 app_config_id, 
                 width=None, 
                 height=None, 
                 view='home', 
                 user=None,
                 **kw):
        super(UserAlertsApp, self).__init__(app_config_id, 
                                             width=width, 
                                             height=height, 
                                             view=view,
                                             user = user,
                                             **kw)

class UserAlertsWidget(Widget):
    params=[]
    template = 'genshi:myfedora.plugins.apps.templates.useralerts'
    javascript = [jquery_js, myfedora_ui_js, myfedora_extensions_js]

    def create_category(self, name, label, url):
        category = {'type': 'alerts_%s' % name,
                    'label': label,
                    'url': url
                    }
        
        return category

    def update_params(self, d):
        super(UserAlertsWidget, self).update_params(d)
        
        user = d.get('user', None)
        categories = []
        
        prefix = ''
        is_auth_user = False
        if not user and tmpl_context.identity:
            user = tmpl_context.identity['person']['username']
            prefix = 'Your'
            is_auth_user = True
        else:
            prefix = "%s's" % user
        
        # just send them to builds for right now
        if is_auth_user:
            baseurl = url('/profile/')
        else:
            baseurl = url('/people/name/%s/' % user)
            
        pkgsurl = baseurl + 'builds/'
            
        categories.append(self.create_category('packages', 
                                               '%s Packages' % prefix, 
                                               pkgsurl)
                         )
        if is_auth_user:
            categories.append(self.create_category('groups', 
                                                   'Your Group Requests', 
                                                   '')
                             )

        d.update({'categories': categories,
                 'user': user,
                 'is_auth_user': is_auth_user,
                 'baseurl': baseurl})

        return d
