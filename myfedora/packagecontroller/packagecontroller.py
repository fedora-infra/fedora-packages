from turbogears import controllers, expose
from turbogears import redirect

from myfedora.urlhandler import KojiURLHandler, BodhiURLHandler, PkgDBURLHandler, BugsURLHandler, URLHandler

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
        dict = {}
        return dict

    @expose(template='myfedora.templates.packages.master')
    def default(self, *args, **kw):
        dict = {}
        dict['package'] = args[0]
        dict['package_url'] = '/packages/' + dict['package']
        dict['my_iframe'] = None

        rurls = []
        route = None
        for resource in reversed(resource_urls):
            urlhandler = resource[1]()
            rurls.append(resource[0])

            # route the url to the correct handler
            try:
                r = args[1].lower()

                if r == resource[0].lower():
                    pkg_url = urlhandler.get_package_url(dict['package'])
                    if urlhandler.get_link_type() == urlhandler.IFRAME_LINK:
                        dict['my_iframe'] = pkg_url
                    elif urlhandler.get_link_type() == urlhandler.INTERNAL_LINK:
                        route = urlhandler.get_route()
            except Exception, e:
                print e 

        dict['resource_urls'] = rurls

        if route:
            dict = route.default(dict, *args, **kw)

        print dict
        return dict 
