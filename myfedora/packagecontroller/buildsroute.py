from route import Route
from myfedora.urlhandler import KojiURLHandler
import koji
import cherrypy

class BuildsRoute(Route):
    def __init__(self):
        Route.__init__(self, "myfedora.templates.packages.builds")

        self.offset = 0 
        self.limit = 10

    def _get_state_img_src(self, state):
        src = ''
        if state == 1:
            src = 'http://koji.fedoraproject.org/koji-static/images/complete.png'
        elif state == 4:
            src = 'http://koji.fedoraproject.org/koji-static/images/canceled.png'
        elif state == 2:
            src = 'http://koji.fedoraproject.org/koji-static/images/deleted.png'
        elif state == 3:
            src = 'http://koji.fedoraproject.org/koji-static/images/failed.png'
        elif state == 0:
            src = 'http://koji.fedoraproject.org/koji-static/images/building.png'
        return src

    def index(self, dict, package, **kw):
        cs = koji.ClientSession(KojiURLHandler().get_xml_rpc_url())
        pkg_id = cs.getPackageID(package)
        # always add 1 to the limit so we know if there should be another page 
        queryOpts = {'offset': self.offset, 
                     'limit': self.limit + 1, 
                     'order': '-creation_time'}
        builds_list = cs.listBuilds(packageID=pkg_id, queryOpts=queryOpts)

        list_count = len(builds_list)

        for build in builds_list:
            # show state icon
            state = build['state']
            build['mf_state_img']= self._get_state_img_src(state)

            # get tag to determine release
            # FIXME: we should add a call to koji to optimize this as a join
            #        or do them as seperate json queries
            tags = cs.listTags(build = build['build_id'])
            build['mf_release'] = tags 

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
        dict['tg_template'] = self.get_default_template()
        dict['current_url'] = cherrypy.request.path

        self.offset = kw.get('offset', self.offset)
        if self.offset:
            self.offset = int(self.offset)

        self.limit = int(kw.get('limit', self.limit))

        direction = kw.get('direction', None)

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
