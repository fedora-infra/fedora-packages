from myfedora.widgets.resourceview import ToolWidget
from datetime import datetime
from tw.forms.datagrid import DataGrid
from myfedora.lib.app_factory import AppFactory
from myfedora.lib.utils import HRElapsedTime
from myfedora.lib.appbundle import AppBundle
import pylons
from tg import url
import koji

class BuildsToolApp(AppFactory):
    entry_name = 'tools.builds'

class BuildsToolWidget(ToolWidget):
    template = 'genshi:myfedora.plugins.apps.tools.templates.builds'
    display_name = "Builds"
    offset = 0
    limit = 10
    requires_data_key = False
    
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
        super(ToolWidget, self).update_params(d)

        # get koji build info
        resourceview =  d['resourceview']
        data_key = d['data_key']
        pkg_id = None
        user_id = None

        # get the list
        cs = koji.ClientSession('http://koji.fedoraproject.org/kojihub')

        queryOpts = {'offset': self.offset, 
                     'limit': self.limit + 1, 
                     'order': '-creation_time'}

        username = None
        if resourceview == 'people_view' or resourceview == 'profile_view':
            user = cs.getUser(data_key)
        
            if resourceview != 'profile_view':
                username = data_key
                
            if user:
                user_id = user['id']
            else:
                return d
                
        elif resourceview == 'packages_view':
            pkg_id = cs.getPackageID(data_key)

        builds_list = cs.listBuilds(packageID=pkg_id,
                                    userID=user_id, 
                                    queryOpts=queryOpts)

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

        d['offset'] = self.offset
        d['limit'] = self.limit

        d['next_disabled'] = 'disabled'
        if list_count > self.limit:
            d['next_disabled'] = ''
            d['builds_list'] = builds_list[0:-1]
        else:
            d['builds_list'] = builds_list

        d['previous_disabled'] = 'disabled'
        if self.offset != 0:
            d['previous_disabled'] = ''

        right_col_apps = AppBundle("rightcol")
        nav_class = pylons.g.apps['packagesnav']
        nav_app = nav_class(None, 
                            '320px', 
                            '200px', 
                            'Home',
                            flags=nav_class.BUILDS_SUBNAV_FLAG,
                            user=username)
        
        right_col_apps.add(nav_app)
        d.update({'rightcol':right_col_apps.serialize_apps(pylons.tmpl_context.w)})

        return d
