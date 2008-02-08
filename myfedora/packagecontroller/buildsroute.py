from route import Route
from myfedora.urlhandler import KojiURLHandler
import koji
import cherrypy

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
        for build in builds_list:
            state = build['state']
            if state == 1:
                build['tg_state_img'] = 'http://koji.fedoraproject.org/koji-static/images/complete.png'
            elif state == 4:
                build['tg_state_img'] = 'http://koji.fedoraproject.org/koji-static/images/canceled.png'
            elif state == 2:
                build['tg_state_img'] = 'http://koji.fedoraproject.org/koji-static/images/deleted.png'
            elif state == 3:
                build['tg_state_img'] = 'http://koji.fedoraproject.org/koji-static/images/failed.png'
            elif state == 0:
                build['tg_state_img'] = 'http://koji.fedoraproject.org/koji-static/images/building.png'

        dict['offset'] = self.offset
        dict['limit'] = self.limit

        list_count = len(builds_list)
 
        dict['next_disabled'] = 'disabled'
        if list_count > self.limit:
            dict['next_disabled'] = ''
            dict['builds_list'] = builds_list[0:-1]
        else:
            dict['builds_list'] = builds_list

        dict['previous_disabled'] = 'disabled'
        if self.offset != 0:
            dict['previous_disabled'] = ''
        

        return dict 

    def default(self, dict, package, *args, **kw):
        print str(args), str(kw)
        dict['tg_template'] = self.get_default_template()
        dict['current_url'] = cherrypy.request.path

        self.offset = kw.get('offset', self.offset)
        if self.offset:
            self.offset = int(self.offset)

        self.limit = int(kw.get('limit', self.limit))

        direction = kw.get('direction', None)
        print "direction: ",direction

        if direction == 'next':
            self.offset += self.limit
        elif direction == 'prev':
            self.offset -= self.limit
            if self.offset < 0:
                self.offset = 0

        count = len(args)

        if count == 0:
            dict = self.index(dict, package, **kw)
        elif count == 1:
            view = args[0] 
        else:
            view = args[0]

        return dict
