from datetime import datetime
from tw.api import Widget
from myfedora.widgets import PagerWidget
from myfedora.lib.app_factory import AppFactory
from myfedora.lib.utils import HRElapsedTime
from pylons import tmpl_context, request
from tg import url
import koji

class BuildsTableApp(AppFactory):
    entry_name = 'buildstable'
    
    def __init__(self, *args, **kw):
        super(BuildsTableApp, self).__init__(*args, **kw)
        # person=None 
        # package=None 
        # profile=None
    
class BuildsTableWidget(Widget):
    template = 'genshi:myfedora.plugins.apps.templates.buildstable_canvas'
    offset = 0
    limit = 7
    
    def __init__(self, *args, **kw):
        super(BuildsTableWidget, self).__init__(*args, **kw)
        self.pager = PagerWidget('pager', parent=self)
    
    def _time_delta_to_date_str(self, start, end):
        datetimestr = ""

        delta = end - start

        if delta.days < 1 and start.day == end.day:
            datetimestr += "Today "
        elif delta.days < 7:
            datetimestr += datetime.strftime(start, "%a ")  
        else:
            datetimestr += datetime.strftime(start, "%b %d @ ")
            if start.year != end.year:
                datetimestr += str(start.year)

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
            elapsed_str += str(days) + "d "

        if hours:
            elapsed_str += str(hours) + "h "

        if minutes:
            elapsed_str += str(minutes) + "m "

        if seconds:
            elapsed_str += str(seconds) + "s "
    
        return elapsed_str

    def _make_delta_timestamps_human_readable(self, start, end):
        result_dict = {
                       'start_time_display':None, 
                       'end_time_display':None
                      }

        parse_format = "%Y-%m-%d %H:%M:%S"

        now = datetime.now()
        start = datetime.strptime(start.split(".")[0], parse_format) 
        start_str = self._time_delta_to_date_str(start, now)
        result_dict['start_time_display'] = start_str

        if end:
            end = datetime.strptime(end.split(".")[0], parse_format)
            end_str = self._time_delta_to_date_str(end, now)
            elapsed_str = self._time_delta_to_elapsed_str(start, end)
            result_dict['end_time_display'] =  end_str + ' (' + elapsed_str.strip() + ')'

        return result_dict

    # FIXME: use local images
    def _get_state_img_src(self, state):
        src = ''
        if state == koji.BUILD_STATES['COMPLETE']:
            src = url('/images/16_success_build.png')
        elif state == koji.BUILD_STATES['CANCELED']:
            src = 'http://koji.fedoraproject.org/koji-static/images/canceled.png'
        elif state == koji.BUILD_STATES['DELETED']:
            src = 'http://koji.fedoraproject.org/koji-static/images/deleted.png'
        elif state == koji.BUILD_STATES['FAILED']:
            src = url('/images/16_failure_build.png')
        elif state == koji.BUILD_STATES['BUILDING']:
            src = 'http://koji.fedoraproject.org/koji-static/images/building.png'
        return src

    def update_params(self, d):
        super(BuildsTableWidget, self).update_params(d)

        offset = self.offset

        page = d.get('page', 1)
        if page:
            try:
                page_num = int(page)
                d['page'] = page_num    
                offset = (page_num - 1) * self.limit
            except:
                d['page'] = 1
        else:
            d['page'] = 1
    
        state = None        
        filter_failed = request.params.get('filter_failed', False)
        filter_successful = request.params.get('filter_successful', False)
        if filter_successful:
            state = koji.BUILD_STATES['COMPLETE']
        
        if filter_failed:
            state = koji.BUILD_STATES['FAILED']
                
        profile = d.get('profile', None)
        person = d.get('person', None)
        package = d.get('package', None)

        # get koji build info
        pkg_id = None
        user_id = None

        # get the list
        cs = koji.ClientSession('http://koji.fedoraproject.org/kojihub')

        countQueryOpts = {'countOnly': True}

        queryOpts = {'offset': offset, 
                     'limit': self.limit, 
                     'order': '-creation_time'}

        username = None
        
        if person:
            username = person
        elif profile and tmpl_context.identity:
            username = tmpl_context.identity['person']['username']
            
        if username:
            user = cs.getUser(username)
            if user:
                user_id = user['id']
            else:
                return d
        
        if package:
            pkg_id = cs.getPackageID(package)

        cs.multicall = True
        cs.listBuilds(packageID=pkg_id,
                      userID=user_id,
                      state=state,
                      queryOpts=countQueryOpts)
        cs.listBuilds(packageID=pkg_id,
                      userID=user_id,
                      state=state,
                      queryOpts=queryOpts)

        results = cs.multiCall()
        builds_list = results[1][0]
        total_count = results[0][0]
        
        last_page = int (total_count / self.limit + 1)
        # process list
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
            try:
                hret = HRElapsedTime()
                hret.set_start_timestr(build['completion_time'])
                hret.set_end_time_to_now()
                finished_line_0 =  hret.get_hr_elapsed_time()
                finished_line_1 =  hret.get_hr_start_time()

                build['finished_line_0'] = finished_line_0
                build['finished_line_1'] = finished_line_1
            except Exception, e:
                build['finished_line_0'] = ''
                build['finished_line_1'] = ''
                
            try:
                hret = HRElapsedTime()
                hret.set_start_timestr(build['creation_time'])
                
                ct = build['completion_time']
                if ct:
                    hret.set_end_timestr(ct)
                else:
                    hret.set_end_time_to_now()
                
                # FIXME: move this into the HRElapsedTime class and refactor method names
                elapsed_build_time = self._time_delta_to_elapsed_str(hret.start, hret.end)
                
                build['elapsed_build_time'] =elapsed_build_time
            except Exception, e:    
                build['elapsed_build_time'] = ''

       
        d['builds_list'] = builds_list
        d['child_args'] = {'pager':{'last_page': last_page,
                                     'page': page,
                                     'parent_dom_id': d['id']
                                   }
                          }

        return d
