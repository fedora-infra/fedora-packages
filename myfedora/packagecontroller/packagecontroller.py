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
        for resource in reversed(resource_urls):
            urlhandler = resource[1]()
            rurls.append(resource[0])

            # set the iframe
            try:
                r = args[1].lower()

                if r == resource[0].lower():
                    urlhandler = resource[1]()
                    pkg_url = urlhandler.get_package_url(dict['package'])
 
                    dict['my_iframe'] = pkg_url 
            except:
                pass

        dict['resource_urls'] = rurls

        return dict 
