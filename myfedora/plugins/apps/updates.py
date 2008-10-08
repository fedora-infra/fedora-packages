import logging
from datetime import datetime
from tw.api import Widget
from myfedora.widgets import PagerWidget
from myfedora.lib.app_factory import AppFactory
from myfedora.lib.utils import HRElapsedTime
from pylons import tmpl_context, request
from tg import url

from myfedora.lib.proxy import BodhiClient

log = logging.getLogger(__name__)

class FedoraUpdatesApp(AppFactory):
    entry_name = 'updates'
    
class FedoraUpdatesWidget(Widget):
    params = {'updates': 'A list of bodhi updates'}
    template = 'genshi:myfedora.plugins.apps.templates.updates_canvas'
    offset = 0
    limit = 10

    def __init__(self, *args, **kw):
        super(FedoraUpdatesWidget, self).__init__(*args, **kw)
        self.pager = PagerWidget('pager', parent=self)

    def update_params(self, d):
        super(FedoraUpdatesWidget, self).update_params(d)

        bodhi = BodhiClient()
        query = {'limit': self.limit}

        person = d.get('person', None) # FIXME we need a bodhi query for this
        
        profile = d.get('profile', None)
        query['mine'] = profile and True or False

        candidates = d.get('candidates')
        if candidates:
            # only show candidates
            pass

        testing = d.get('testing')
        if testing:
            query['status'] = 'testing'

        package = d.get('package')
        if package:
            query['package'] = package

        d['updates'] = bodhi.query(**query)

        # Convert the timestamps to human readable ages, and set the
        # karma icons appropriately
        elapsed_time = HRElapsedTime()
        for update in d['updates']['updates']:
            elapsed_time.set_start_timestr(update['date_submitted'])
            elapsed_time.set_end_time_to_now()
            update['age'] = elapsed_time.get_hr_elapsed_time()
            if update['karma'] > 1:
                update['karmaimg'] = 'karma1.png'
            elif update['karma'] < -1:
                update['karmaimg'] = 'karma-1.png'
            else:
                update['karmaimg'] = 'karma0.png'
