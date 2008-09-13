from tw.api import Widget, js_function
from tw.jquery import JQuery,jquery_js
from myfedora.lib.app_factory import AppFactory
from myfedora.lib.proxy import PkgdbClient
from myfedora.lib.utils import odict

from pylons import app_globals, request, tmpl_context
from tg import url

from urlparse import urlparse

class PackagesNavApp(AppFactory):
    entry_name = 'packagesnav'
    
    UPDATES_SUBNAV_FLAG = 1 << 0
    BUILDS_SUBNAV_FLAG = 1 << 1
    
    def __init__(self, 
                 app_config_id, 
                 width=None, 
                 height=None, 
                 view='home', 
                 flags=0,
                 user=None,
                 **kw):
        super(PackagesNavApp, self).__init__(app_config_id, 
                                             width=width, 
                                             height=height, 
                                             view=view,
                                             flags = flags,
                                             user = user,
                                             **kw)

class PackagesNavWidget(Widget):
    params=[]
    template = 'genshi:myfedora.plugins.apps.templates.packagesnav'
    javascript = [jquery_js]

    def create_subnav_item(self, name, label, url, jscallback):
        if jscallback:
            jscallback += '(%s);' % name         
        
        #TODO: URL rewriting
        
        return {'label': label,
                'url': url,
                'jscallback': jscallback}

    def create_subnav(self, d, url, jscallback):
        subnav = odict()
        
        try:
            flags = d.get('flags', 0)
            flags = int(flags)
        except:
            flags = 0
        
        
        if flags & PackagesNavApp.BUILDS_SUBNAV_FLAG:
            name = 'failed_builds'
            label = 'Failed Builds'
            subnav[name] = self.create_subnav_item(name,
                                                   label,
                                                   url,
                                                   jscallback)
            name = 'successful_builds'
            label = 'Successful Builds'
            subnav[name] = self.create_subnav_item(name,
                                                   label,
                                                   url,
                                                   jscallback)
            
            
        if flags & PackagesNavApp.UPDATES_SUBNAV_FLAG:
            name = 'unpushed_updates'
            label = 'Unpushed Updates'
            subnav[name] = self.create_subnav_item(name,
                                                   label,
                                                   url,
                                                   jscallback)
            
            name = 'pending_updates'
            label = 'Pending Updates'
            subnav[name] = self.create_subnav_item(name,
                                                   label,
                                                   url,
                                                   jscallback)
            
            name = 'testing_updates'
            label = 'Testing Updates'
            subnav[name] = self.create_subnav_item(name,
                                                   label,
                                                   url,
                                                   jscallback)

            name = 'stable_updates'
            label = 'Stable Updates'
            subnav[name] = self.create_subnav_item(name,
                                                   label,
                                                   url,
                                                   jscallback)
            
        return subnav
        
    def create_nav_item(self, d, label, url=None, jscallback=None):
        subnav = self.create_subnav(d, url, jscallback)
        navelement = {'label': label,
                      'url': url,
                      'jscallback': jscallback,
                      'subnav': subnav}
        
        return navelement


    def update_params(self, d):
        super(PackagesNavWidget, self).update_params(d)
        
        nav = odict()
        
        if tmpl_context.identity:
            user = tmpl_context.identity['person']['username']
            
            user = d.get('user', None)
            if not user:
                user = 'I'
            nav['own']= self.create_nav_item(d, 'Packages %s Own' % (user))
            nav['maintain']= self.create_nav_item(d, 'Packages %s Maintain' % (user))
            
        nav['all']= self.create_nav_item(d, 'All Packages')
        
        d.update({'nav': nav})
        print (d)
        return d
