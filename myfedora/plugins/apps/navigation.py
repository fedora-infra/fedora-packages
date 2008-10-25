from tw.api import Widget, js_function
from tw.jquery import JQuery,jquery_js
from myfedora.lib.app_factory import AppFactory
from pylons import app_globals
from pylons import request
from tg import url

from urlparse import urlparse

class NavigationApp(AppFactory):
    entry_name = 'navigation'

class NavigationWidget(Widget):
    params=[]
    template = 'genshi:myfedora.plugins.apps.templates.navigation'
    javascript = [jquery_js]

    def update_params(self, d):
        super(NavigationWidget, self).update_params(d)
        
        # right now just work with resource views but we should also work with
        # user defined links and other controllers
        rvs = app_globals.resourceviews
        
        url_path = urlparse(request.environ['PATH_INFO'])[2]
        
        has_active = False
        nav = []
        for view in rvs.itervisible():
            item = {'label': '',
                    'icon': None,
                    'href': '',
                    'state': 'inactive'}
            
            item['label'] = view.display_name
            tool_dir = '/' + view.entry_name
            item['href'] = url(tool_dir)

            if url_path.startswith(tool_dir):
                item['state'] = 'active'
                has_active = True
            
            nav.append(item)
        
        state = 'inactive'
        if not has_active:
            state = 'active'
             
        nav.insert(0, {'label': 'Home',
                       'icon': None,
                       'href':url('/'),
                       'state': state
                       }
                  )
        
        d.update({'navigation_list': nav})
        return d
