from datetime import datetime
from tw.api import Widget
from myfedora.lib.app_factory import AppFactory
from myfedora.lib.utils import HRElapsedTime
from myfedora.lib.proxy import FasClient
from myfedora.plugins.identity import bloginfo
from pylons import tmpl_context
from tg import url

class PeopleAlphaListApp(AppFactory):
    entry_name = 'peoplealphalist'
    
    def __init__(self, *args, **kw):
        super(PeopleAlphaListApp, self).__init__(*args, **kw)
        # search='a*'
    
class PeopleAlphaListWidget(Widget):
    template = 'mako:/myfedora/plugins/apps/templates/peoplealphalist.html'

    def update_params(self, d):
        super(PeopleAlphaListWidget, self).update_params(d)
                 
        search = d.get('search', 'a*')

        # get the list
        cs = FasClient()
        results = cs.user_list(search)
        for person in results['people']:
            user_list = []
            user_name = person['username']
            
            # get hackergotchi
            b = bloginfo.get_metadata(user_name)
            if b:
                person.update(b)
                
            # calc time
            hret = HRElapsedTime()
            hret.set_start_timestr(person['last_seen'])
            hret.set_end_time_to_now()
            line0 = hret.get_hr_elapsed_time()
            line1 = hret.get_hr_start_time()
                
            person.update({'last_seen_hr_0':line0,'last_seen_hr_1':line1})
            person['url'] = url('/people/name/%s' % user_name)

        d.update({'people':results['people']})
        
        return d
