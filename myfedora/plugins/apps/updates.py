# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; version 2 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Library General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
#
# Copyright 2008  Red Hat, Inc
# Authors: Luke Macken <lmacken@redhat.com>

import koji
import logging

from tg import url, expose, validate, config
from tw.api import Widget, WidgetsList, js_callback, js_function
from tw.forms import (TableForm, TextField, SingleSelectField, TextArea,
                      CheckBox)
from tw.jquery.activeform import AjaxForm

from pylons import tmpl_context, request
from formencode import validators, All

from myfedora.widgets import PagerWidget
from myfedora.lib.app_factory import AppFactory
from myfedora.lib.base import Controller
from myfedora.lib.utils import HRElapsedTime
from myfedora.lib.proxy import BodhiClient
from myfedora.controllers.resourceview import ResourceViewController

log = logging.getLogger(__name__)


class NewUpdateWidget(AjaxForm):
    #success = 'newupdate_success'
    action = 'save'
    class fields(WidgetsList):
        builds = TextField(validator=All(validators.NotEmpty(),
                           validators.UnicodeString()), disabled=True)
        bugs = TextField(validator=validators.UnicodeString())
        types = ('bugfix', 'enhancement', 'security', 'newpackage')
        type = SingleSelectField(options=types,
                                 validator=validators.OneOf(types))
        requests = ('Testing', 'Stable')
        request = SingleSelectField(options=requests,
                                    validator=validators.OneOf(requests))
        notes = TextArea(validator=validators.UnicodeString())
        #autokarma = CheckBox(validator=validators.StringBool())
        #reboot = CheckBox(validator=validators.StringBool())


new_update_form = NewUpdateWidget('new_update_form', target='output')

bodhi = BodhiClient()


class FedoraUpdatesController(Controller):

    @expose('genshi:myfedora.plugins.apps.templates.updateform')
    def new(self, **kw):
        tmpl_context.new_update_form = new_update_form
        return dict(value=kw)

    @expose('json')
    @validate(new_update_form, error_handler=new)
    def save(self, builds, type, bugs, request, notes):
        log.debug('save(%s)' % locals())
        results = bodhi.save(builds=builds, type_=type, bugs=bugs,
                             request=request.lower(), notes=notes)
        log.debug('results = %r' % results)
        return results

    @expose('json')
    def request(self, update, action):
        """ Request a specified action on a given update """
        log.debug('request(%s, %s)' % (update, action))
        response = bodhi.request(update, action)
        if 'message' in response:
            response['tg_flash'] = response['message']
        return response


class FedoraUpdatesApp(AppFactory):
    entry_name = 'updates' 
    controller = FedoraUpdatesController


class FedoraUpdateCandidatesWidget(Widget):
    """ A widget for displaying candidate update builds """
    params = {'builds': 'A list of koji builds'}
    template = 'genshi:myfedora.plugins.apps.templates.candidates_canvas'

    def update_params(self, d):
        super(FedoraUpdatesWidget, self).update_params(d)

        koji_session = koji.ClientSession(config['koji_hub'])

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
    template = 'mako:/myfedora/plugins/apps/templates/updates_canvas.html'
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
        query = {'limit': self.limit, 'page': page_num}

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

        # filters
        if request.params.get('filter_security'):
            query['type_'] = 'security'
        for status in ('pending', 'testing', 'stable'):
            if request.params.get('filter_%s' % status):
                query['status'] = status

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

        This entails converting the timestamps to human readable ages,
        setting the karma icons, and determining all available actions.

        Ideally, bodhi should be figuring this stuff out for us.  A ticket is
        opened to move this feature upstream.

            https://fedorahosted.org/bodhi/ticket/255
        """
        elapsed_time = HRElapsedTime()

        for update in updates['updates']:

            # Age
            elapsed_time.set_start_timestr(update['date_submitted'])
            elapsed_time.set_end_time_to_now()
            update['age'] = elapsed_time.get_hr_elapsed_time()

            # Karma icons
            if update['karma'] > 1:
                update['karmaimg'] = 'karma1.png'
            elif update['karma'] < -1:
                update['karmaimg'] = 'karma-1.png'
            else:
                update['karmaimg'] = 'karma0.png'

            # Actions
            update['actions'] = []
            if update['status'] == 'testing':
                update['actions'].append(('unpush', 'Unpush'))
                update['actions'].append(('stable', 'Push to stable'))
            if update['status'] == 'pending':
                update['actions'].append(('testing', 'Push to testing'))
                update['actions'].append(('stable', 'Push to stable'))
            if update['request']:
                update['actions'].append(('revoke', 'Cancel push'))
