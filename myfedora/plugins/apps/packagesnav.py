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
                 package=None,
                 **kw):
        super(PackagesNavApp, self).__init__(app_config_id, 
                                             width=width, 
                                             height=height, 
                                             view=view,
                                             flags = flags,
                                             user = user,
                                             package = package,
                                             **kw)

class PackagesNavWidget(Widget):
    params=[]
    template = 'genshi:myfedora.plugins.apps.templates.packagesnav'
    javascript = [jquery_js]
    
    def _construct_query_string(self, req_params, **params):
        if not req_params and not params:
            return ''
        
        result = '?'
        
        for (key, value) in req_params.iteritems():
            result += '%s=%s&' % (key,value)
            
        for (key, value) in params.iteritems():
            result += '%s=%s&' % (key,value)
        
        return result[:-1]

    def create_subnav_item(self, name, label, url, jscallback, req_params={}):
        if jscallback:
            jscallback += '(%s);' % name
        
        if url:   
            url += self._construct_query_string(req_params)
        
        return {'label': label,
                'url': url,
                'jscallback': jscallback}

    def create_subnav(self, d, url, jscallback, req_params={}):
        subnav = odict()
            
        try:
            flags = d.get('flags', 0)
            flags = int(flags)
        except:
            flags = 0
        
        
        if flags & PackagesNavApp.BUILDS_SUBNAV_FLAG:
            name = 'failed_builds'
            label = 'Failed Builds'
            params = {'filter_failed': 'true'}
            params.update(req_params)
            subnav[name] = self.create_subnav_item(name,
                                                   label,
                                                   url,
                                                   jscallback,
                                                   req_params=params)
            name = 'successful_builds'
            label = 'Successful Builds'
            
            params = {'filter_successful': 'true'}
            params.update(req_params)
            subnav[name] = self.create_subnav_item(name,
                                                   label,
                                                   url,
                                                   jscallback,
                                                   req_params=params)
            
            
        if flags & PackagesNavApp.UPDATES_SUBNAV_FLAG:
            name = 'unpushed_updates'
            label = 'Unpushed Updates'
            
            params = {'filter_unpushed': 'true'}
            params.update(req_params)
            
            subnav[name] = self.create_subnav_item(name,
                                                   label,
                                                   url,
                                                   jscallback,
                                                   req_params=params)
            
            name = 'pending_updates'
            label = 'Pending Updates'
            
            params = {'filter_pending': 'true'}
            params.update(req_params)
            
            subnav[name] = self.create_subnav_item(name,
                                                   label,
                                                   url,
                                                   jscallback,
                                                   req_params=params)
            
            name = 'testing_updates'
            label = 'Testing Updates'
            
            params = {'filter_testing': 'true'}
            params.update(req_params)
    
            subnav[name] = self.create_subnav_item(name,
                                                   label,
                                                   url,
                                                   jscallback,
                                                   req_params=params)

            name = 'stable_updates'
            label = 'Stable Updates'
            
            params = {'filter_stable': 'true'}
            params.update(req_params)
            
            subnav[name] = self.create_subnav_item(name,
                                                   label,
                                                   url,
                                                   jscallback,
                                                   req_params=params)
            
        return subnav
        
    def create_nav_item(self, d, label, url=None, jscallback=None, req_params={}):
        subnav = self.create_subnav(d, url, jscallback, req_params=req_params)
        
        if url:
            url += self._construct_query_string(req_params)
            
        navelement = {'label': label,
                      'url': url,
                      'jscallback': jscallback,
                      'subnav': subnav}
        
        return navelement


    def update_params(self, d):
        super(PackagesNavWidget, self).update_params(d)
        
        tool = d.get('tool', 'builds')
        
        nav = odict()
        tool_url = url('/%s/%s/' % (tmpl_context.resource_view, tool))
        
        nav['all']= self.create_nav_item(d, 'All Packages', tool_url)
        
        package = d.get('package', None)
        if package:
            package_url = url('/%s/name/%s/%s/' % (tmpl_context.resource_view, package, tool))
            nav['dbus']= self.create_nav_item(d, package + ' Packages', package_url)
        
        if tmpl_context.identity:
            user = tmpl_context.identity['person']['username']
            
            user = d.get('user', None)
            if not user:
                user = 'I'
                
            profile_url = url('/profile/%s/' % (tool))
            nav['own']= self.create_nav_item(d, 'Packages %s Own' % (user), 
                                             profile_url, 
                                             req_params = {'filter_own': 'true'})
            nav['maintain']= self.create_nav_item(d, 'Packages %s Maintain' % (user),
                                                  profile_url, 
                                                  req_params = {'filter_maintain':'true'})
            
        
        
        d.update({'nav': nav})

        return d
