import koji

from tg import url, expose
from tw.api import Widget, WidgetsList
from tw.forms import (TableForm, TextField, SingleSelectField, TextArea,
                      CheckBox)
from pylons import tmpl_context, request

from myfedora.widgets import PagerWidget
from myfedora.lib.app_factory import AppFactory
from myfedora.lib.base import Controller
from myfedora.lib.utils import HRElapsedTime
from myfedora.lib.proxy import BodhiClient
from myfedora.controllers.resourceview import ResourceViewController

KOJI_URL = 'http://koji.fedoraproject.org/kojihub'

class NewUpdateWidget(TableForm):
    """
    TODO:
        - use a tw.jquery ajax form?
        - display a list of potential bugzillas for this update
    """
    class fields(WidgetsList):
        title = TextField()
        bugs = TextField()
        types = ((1, 'enhancement'),
                 (2, 'bugfix'),
                 (3, 'security'),
                 (4, 'newpackage'))
        type = SingleSelectField(options=types)
        request = SingleSelectField(options=((1, 'Testing'), (2, 'Stable')))
        notes = TextArea()
        # karma automation
        # recommend reboot

new_update_form = NewUpdateWidget('new_update_form')


class FedoraUpdatesController(ResourceViewController):

    @expose('genshi:myfedora.plugins.apps.templates.updateform')
    def updateform(self):
        tmpl_context.new_update_form = new_update_form
        return dict()


class FedoraUpdatesApp(AppFactory):
    entry_name = 'updates'
    controller = FedoraUpdatesController


class FedoraUpdateCandidatesWidget(Widget):
    """ A widget for displaying candidate update builds """
    params = {'builds': 'A list of koji builds'}
    template = 'genshi:myfedora.plugins.apps.templates.candidates_canvas'

    def update_params(self, d):
        super(FedoraUpdatesWidget, self).update_params(d)

        bodhi = BodhiClient()
        koji_session = koji.ClientSession(KOJI_URL)

        person = d.get('person')
        if not person:
            raise Exception('You must be logged in to view your '
                            'candidate updates')

        d['updates'] = []
        for tag in [tag + '-updates-candidate' for tag in
                    bodhi.send_request('dist_tags')[1]['tags']]:
            for build in koji_session.listTagged(tag, latest=True):
                if build['owner_name'] == person:
                    d['updates'].append(build)


class FedoraUpdatesWidget(Widget):
    """ A widget for displaying a list of bodhi updates """
    params = {'updates': 'A list of bodhi updates'}
    template = 'genshi:myfedora.plugins.apps.templates.updates_canvas'
    limit = 10

    def __init__(self, *args, **kw):
        super(FedoraUpdatesWidget, self).__init__(*args, **kw)
        self.pager = PagerWidget('pager', parent=self)

    def update_params(self, d):
        super(FedoraUpdatesWidget, self).update_params(d)

        page = d.get('page', 1)
    
        try:
            page_num = int(page)
            d['page'] = page_num    
            offset = (page_num - 1) * self.limit
        except:
            d['page'] = 1

        bodhi = BodhiClient()
        query = {'limit': self.limit,
                 'page':page_num
                 }

        username = d.get('person')
        if username:
            query['username'] = username
        
        profile = d.get('profile', None)
        query['mine'] = profile and True or False

        testing = d.get('testing')
        if testing:
            query['status'] = 'testing'

        package = d.get('package')
        if package:
            query['package'] = package

        d['updates'] = bodhi.query(**query)
        
        total_count = d['updates']['num_items']
        last_page = int (total_count / self.limit + 1)
        
        self._postprocess_updates(d['updates'])
        d['child_args'] = {'pager':{'last_page': last_page,
                                     'page': page,
                                     'parent_dom_id': d['id']
                                   }
                          }

    def _postprocess_updates(self, updates):
        """ Perform post-processing on a list of bodhi updates.

        This entails Converting the timestamps to human readable ages, and
        set the karma icons appropriately.
        """
        elapsed_time = HRElapsedTime()
        for update in updates['updates']:
            elapsed_time.set_start_timestr(update['date_submitted'])
            elapsed_time.set_end_time_to_now()
            update['age'] = elapsed_time.get_hr_elapsed_time()
            if update['karma'] > 1:
                update['karmaimg'] = 'karma1.png'
            elif update['karma'] < -1:
                update['karmaimg'] = 'karma-1.png'
            else:
                update['karmaimg'] = 'karma0.png'

