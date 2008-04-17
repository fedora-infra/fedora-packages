from myfedora.mfquery.bodhi_query import BodhiQuery
from route import Route

bodhi_query = BodhiQuery()

class UpdatesRoute(Route):
    def __init__(self):
        Route.__init__(self, "myfedora.templates.packages.updates")

    def index(self, dict, package, **kw):
        result = bodhi_query.get_info(True, package=package)
        dict['tg_template'] = self.get_default_template()
        dict['current_url'] = cherrypy.request.path
        
        result.update(dict)
        print result
        return result

    def default(self, dict, package, **kw):
        return self.index(dict, package, **kw)
