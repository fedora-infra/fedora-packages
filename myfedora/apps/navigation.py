from tw.api import Widget, js_function
from tw.jquery import JQuery,jquery_js
from myfedora.lib.app_factory import AppFactory
from pylons import app_globals
from tg import url

class NavigationApp(AppFactory):
    entry_name = 'navigation'

class NavigationWidget(Widget):
    params=[]
    template = 'genshi:myfedora.apps.templates.navigation'
    javascript = [jquery_js]

    def update_params(self, d):
        super(NavigationWidget, self).update_params(d)
        
        # right now just work with resource views but we should also work with
        # user defined links and other controllers
        rvs = app_globals.resourceviews
        nav = []
        for name, view in rvs.iteritems():
            item = {'label': '',
                    'icon': None,
                    'href': ''}
            
            item['label'] = view.display_name
            item['href'] = url('/' + view.entry_name)
            nav.append(item)
        
        
        d.update({'navigation_list': nav})
        return d
