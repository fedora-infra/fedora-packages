from turbogears import controllers, expose
from turbogears import redirect

from myfedora.urlhandler import KojiURLHandler, BodhiURLHandler, PkgDBURLHandler, BugsURLHandler, URLHandler

import cherrypy

class InfoURLHandler(URLHandler):
    def __init__(self):
        URLHandler.__init__(self)

        self.set_base_url('/packages')

resource_urls = (('Info', InfoURLHandler),
                 ('Builds', KojiURLHandler),
                 ('Updates', BodhiURLHandler),
                 ('Permissions', PkgDBURLHandler),
                 ('Bugs', BugsURLHandler))

class PackageController(controllers.Controller):
    @expose(template='myfedora.templates.packages.master')
    def index(self):
        dict = {'package':'',
                'resource_urls': resource_urls}

        return dict

    @expose(template='myfedora.templates.packages.iframe')
    def default(self, *args, **kw):
        dict = {}

        last_resource = ''
        if cherrypy.request.simple_cookie.has_key('packages-last-resource'):
            last_resource = cherrypy.request.simple_cookie['packages-last-resource'].value

        count = len(args)

        package_name = args[0]

        if count == 1 and last_resource:
            raise redirect(package_name + '/' + last_resource)

        dict['package'] = package_name
        
        dict['package_url'] = '/packages/' + package_name 
        dict['my_iframe'] = None

        rurls = []
        route = None
        current_resource = ''
        for resource in reversed(resource_urls):
            urlhandler = resource[1]()
            rurls.append(resource[0])

            # route the url to the correct handler
            try:
                r = args[1].lower()

                if r == resource[0].lower():
                    current_resource = args[1] 
                    pkg_url = urlhandler.get_package_url(dict['package'])
                    if urlhandler.get_link_type() == urlhandler.IFRAME_LINK:
                        dict['my_iframe'] = pkg_url
                    elif urlhandler.get_link_type() == urlhandler.INTERNAL_LINK:
                        route = urlhandler.get_route()
            except Exception, e:
                print e 

        dict['resource_urls'] = rurls
        cherrypy.response.simple_cookie['packages-last-resource'] = current_resource
        cherrypy.response.simple_cookie['packages-last-resource']['path']='/packages'
        if route:
            package = args[0]
            dict = route.default(dict, package, *args[2:], **kw)

        return dict 
