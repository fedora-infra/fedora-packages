from route import Route
from myfedora.urlhandler import KojiURLHandler
import koji

class BuildsRoute(Route):
    def __init__(self):
        Route.__init__(self, "myfedora.templates.packages.builds")

        self.offset = 0
        self.limit = 10

    def index(self, dict, package, **kw):
        cs = koji.ClientSession(KojiURLHandler().get_xml_rpc_url())
        pkg_id = cs.getPackageID(package)
       
        # always add 1 to the limit so we know if there should be another page 
        queryOpts = {'offset': self.offset, 'limit': self.limit + 1}
        builds_list = cs.listBuilds(packageID=pkg_id, queryOpts=queryOpts)

        dict['offset'] = self.offset
        dict['limit'] = self.limit
        dict['builds_list'] = builds_list[0:-1]

        list_count = len(builds_list)

        has_more = False
        if list_count > self.limit:
            has_more = True

        dict['has_more'] = has_more

        return dict 

    def default(self, dict, package, *args, **kw):
        dict['tg_template'] = self.get_default_template()

        self.offset = int(kw.get('offset', self.offset))
        self.limit = int(kw.get('limit', self.limit))

        count = len(args)

        if count == 0:
            self.index(dict, package, **kw)
        elif count == 1:
            view = args[0] 
        else:
            view = args[0]

        return dict
