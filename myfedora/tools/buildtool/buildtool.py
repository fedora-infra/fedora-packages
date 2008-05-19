from myfedora.urlhandler import KojiURLHandler
from myfedora.plugin import Tool
from turbogears import expose


from datetime import datetime
import koji
import cherrypy


class BuildsTool(Tool):
    def __init__(self, parent_resource):
        Tool.__init__(self, parent_resource,
                            'Builds',
                            'builds',
                            'Shows the current builds',
                            '''The build tool allows you to look at
                               and manipulate build data
                            ''',
                            ['packages'],
                            [])

        self.offset = 0 
        self.limit = 10

    def _time_delta_to_date_str(self, start, end):
        datetimestr = ""

        delta = end - start

        if delta.days < 1 and start.tm_mday == end.tm_mday:
            datetimestr += "Today "
        elif delta.days < 7:
            datetimestr += datetime.strftime(start, "%a ")  
        else:
            datetimestr += datetime.strftime(start, "%b %d ")
            #if start.tm_year != end.tm_year:
            #    datetimestr += str(start.tm_year)

        datetimestr +=  datetime.strftime(start,"%H:%M")

        return datetimestr

    def _time_delta_to_elapsed_str(self, start, end):
        elapsed_str = ""

        delta = end - start

        days = delta.days
        hours = int(delta.seconds / 3600)
        minutes = int((delta.seconds - hours * 3600) / 60)
        seconds = delta.seconds - minutes * 60

        if days:
            elapsed_str += str(days) + " day"
            if days > 1:
                elapsed_str += "s "
            else:
                elapsed_str += " "

        if hours:
            elapsed_str += str(hours) + " hour"
            if hours > 1:
                elapsed_str += "s "
            else:
                elapsed_str += " "

        if minutes:
            elapsed_str += str(minutes) + " minute"
            if minutes > 1:
                elapsed_str += "s "
            else:
                elapsed_str += " "

        if seconds:
            elapsed_str += "and " + str(seconds) + " second"
            if seconds > 1:
                elapsed_str += "s "
            else:
                elapsed_str += " "

        return elapsed_str

    def _make_delta_timestamps_human_readable(self, start, end):
        result_dict = {
                       'start_time_display':None, 
                       'end_time_display':None
                      }

        parse_format = "%Y-%m-%d %H:%M:%S"

        start = datetime.strptime(start.split(".")[0], parse_format) 
        end = datetime.strptime(end.split(".")[0], parse_format)
        now = datetime.now()

        start_str = self._time_delta_to_date_str(start, now)
        end_str = self._time_delta_to_date_str(end, now)
        elapsed_str = self._time_delta_to_elapsed_str(start, end)
        
        result_dict['start_time_display'] = start_str
        result_dict['end_time_display'] =  end_str + '(' + elapsed_str + ')'

        return result_dict

    def _get_state_img_src(self, state):
        src = ''
        if state == koji.BUILD_STATES['COMPLETE']:
            src = 'http://koji.fedoraproject.org/koji-static/images/complete.png'
        elif state == koji.BUILD_STATES['CANCELED']:
            src = 'http://koji.fedoraproject.org/koji-static/images/canceled.png'
        elif state == koji.BUILD_STATES['DELETED']:
            src = 'http://koji.fedoraproject.org/koji-static/images/deleted.png'
        elif state == koji.BUILD_STATES['FAILED']:
            src = 'http://koji.fedoraproject.org/koji-static/images/failed.png'
        elif state == koji.BUILD_STATES['BUILDING']:
            src = 'http://koji.fedoraproject.org/koji-static/images/building.png'
        return src

    @expose(Tool.local_template('builds'))
    def index(self, package, **kw):
        dict = self.get_parent_resource().get_template_globals(package)

        cs = koji.ClientSession(KojiURLHandler().get_xml_rpc_url())
        
        pkg_id = None
        if (package):
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
            tags = '' #cs.listTags(build = build['build_id'])
            build['mf_release'] = tags
            build['mf_arches'] = []
            if tags:
                arches = tags[0]['arches']
                if arches:
                    arches = arches.split(' ')
                    arches.append('src')
                    build['mf_arches'] = arches

            # convert timestamps to human readable entries
            time_dict = self._make_delta_timestamps_human_readable(
                            build['creation_time'],
                            build['completion_time'])

            build['creation_time'] = time_dict['start_time_display']
            build['completion_time'] = time_dict['end_time_display']

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

    @expose('myfedora.tools.buildtool.templates.builds')
    def default(self, package, *args, **kw):
        dict = get_parent_resource().get_template_globals(package)        

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
