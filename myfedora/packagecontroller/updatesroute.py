from myfedora.mfquery.bodhi_query import BodhiQuery
from route import Route

bodhi_query = BodhiQuery()

class UpdatesRoute(Route):
    def __init__(self):
        Route.__init__(self, "myfedora.templates.packages.updates")

    def index(self, dict, package, **kw):
        result = bodhi_query.get_info(dict)
        print result

        return result
