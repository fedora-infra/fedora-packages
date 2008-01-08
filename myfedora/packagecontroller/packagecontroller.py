from turbogears import controllers, expose
from turbogears import redirect

from myfedora.urlhandler import KojiURLHandler, BodhiURLHandler, PkgDBURLHandler, BugsURLHandler, URLHandler

class InfoURLHandler(URLHandler):
    def __init__(self):
        URLHandler.__init__(self)

        self.set_base_url('/packages')

resource_urls = {'info':('Info', InfoURLHandler),
                 'builds':('Builds', KojiURLHandler),
                 'updates':('Updates', BodhiURLHandler),
                 'acls':('ACLs', PkgDBURLHandler),
                 'bugs':('Bugs', BugsURLHandler)}

class PackageController(controllers.Controller):
    @expose(template='myfedora.templates.packages.index')
    def index(self):
        dict = {}
        return dict

    @expose(template='myfedora.templates.packages.index')
    def default(self, *args, **kw):
        dict = {}
        dict['package'] = args[0]
        dict['package_url'] = '/packages/' + dict['package']
        dict['my_iframe'] = None

        rurls = {}
        for key in resource_urls.keys():
            resource = resource_urls[key]
            urlhandler = resource[1]()
            pkg_url = urlhandler.get_package_url(dict['package'])
            url_mapping = (resource[0], pkg_url)
            rurls[key] = url_mapping

        print rurls

        dict['resource_urls'] = rurls

        try:
            r = args[1].lower()

            dict['my_iframe'] = rurls[r][1]
        except:
            pass

        return dict 
