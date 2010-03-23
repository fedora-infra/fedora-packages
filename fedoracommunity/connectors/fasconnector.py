
# This file is part of Fedora Community.
# Copyright (C) 2008-2010  Red Hat, Inc.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from moksha.connector import IConnector, ICall, IQuery, ISearch, ParamFilter
from pylons import config, cache
from fedora.client import ProxyClient, ServerError
from fedora.client.fas2 import AccountSystem
from moksha.lib.helpers import DateTimeDisplay
import time

USERINFO_CACHE_TIMEOUT= 60 * 5 # s * m = 5 minutes
_fas_minimal_user = config.get('fedoracommunity.connector.fas.minimal_user_name')
_fas_minimal_pass = config.get('fedoracommunity.connector.fas.minimal_user_password')

class UserNotFoundError(LookupError):
    pass

class FasConnector(IConnector, ICall, ISearch, IQuery):
    _method_paths = {}
    _query_paths = {}

    def __init__(self, environ=None, request=None):
        super(FasConnector, self).__init__(environ, request)
        self._fas_client = ProxyClient(self._base_url,
                                       session_as_cookie=False,
                                       insecure = self._insecure)

    # IConnector
    @classmethod
    def register(cls):
        cls._base_url = config.get('fedoracommunity.connector.fas.baseurl',
                                   'https://admin.fedoraproject.org/accounts')

        check_certs = config.get('fedora.clients.check_certs', 'True').lower()
        if check_certs in ('false', '0', 'no'):
            insecure = True
        else:
            # fail safe
            insecure = False

        cls._insecure = insecure

        cls.register_query_usermemberships()
        cls.register_query_userinfo()
        cls.register_query_people()
        cls.register_search_people()

    def request_data(self, resource_path, params, _cookies):
        if self._environ:
            identity = self._environ.get('repoze.who.identity')
            auth_params={}
        else:
            identity = None
        if identity:
            session_id = identity.get('session_id')
            auth_params={'session_id': session_id}
        else:
            # use the minimal login if available
            auth_params={'username': _fas_minimal_user, 'password': _fas_minimal_pass}

        return self._fas_client.send_request(resource_path,
                                             auth_params = auth_params,
                                             req_params = params)

    def introspect(self):
        # FIXME: return introspection data
        return None

    #ICall
    def call(self, resource_path, params=None, _cookies=None):
        # proxy client only returns structured data so we can pass
        # this off to request_data but we should fix that in ProxyClient
        if not params:
            params = {}
        return self.request_data(resource_path, params, _cookies)

    def create_fas_object(self):
        if self._environ:
            identity = self._environ.get('repoze.who.identity')
        else:
            identity = None
        if identity:
            return AccountSystem(base_url=self._base_url,
                                 session_id=identity.get('session_id'))
        else:
            return AccountSystem(base_url=self._base_url,
                                 username=_fas_minimal_user,
                                 password=_fas_minimal_pass)

    def request_user_view(self, user):
        try:
            view = self.call('user/view', {'username': user})
        except ServerError, e:
            raise UserNotFoundError('User %s can not be found.' % user)

        if not view:
            return None

        view = view[1]
        extra = {'cla':view['cla'],
                 'admin':view['admin'],
                 'personal':view['personal']
                 }

        view = view['person']
        view.update(extra)


        # Check to see if this user has enabled VOIP for their account
        #config = self._fas_client.send_request('config/list/%s/asterisk/enabled'
        #                                       % user, req_params={},
        #                                       auth_params={
        #                                          'username': _fas_minimal_user,
        #                                          'password': _fas_minimal_pass
        #                                          })
        #print config

        return view

    def get_user_view(self, user, invalidate=False):
        if not isinstance(user, basestring):
            return None

        fas_cache = cache.get_cache('fas')

        key = '_fas_user_info_' + user
        if invalidate:
            fas_cache.remove_value(key)
        try:
             info = fas_cache.get_value(key = key ,
                                   createfunc=lambda : self.request_user_view(user),
                                   type="memory",
                                   expiretime=USERINFO_CACHE_TIMEOUT)
        except UserNotFoundError, e:
            return {'error_type': e.__class__.__name__,
                    'error': str(e)
                    }

        return info

    # ISearch
    @classmethod
    def register_search_people(cls):
        path = cls.register_search_path(
                      'search_people',
                      cls.search_people,
                      primary_key_col = 'username',
                      default_sort_col = 'username',
                      default_sort_order = -1,
                      can_paginate = True)

        # make human name weighted more
        path.register_column('human_name',
                        default_visible = True,
                        can_sort = False,
                        can_filter_wildcards = False)

        path.register_column('username',
                        default_visible = True,
                        can_sort = False,
                        can_filter_wildcards = False)

    def search_people(self, search_term):
        result = self.call('user/list',
                           params={'search': '*' + search_term + '*'})
        return result[1]['people']

    # IQuery
    @classmethod
    def register_query_people(cls):
        path = cls.register_query(
                      'query_people',
                      cls.query_people,
                      primary_key_col = 'username',
                      default_sort_col = 'username',
                      default_sort_order = -1,
                      can_paginate = True)

        path.register_column('username',
                        default_visible = True,
                        can_sort = False,
                        can_filter_wildcards = False)
        path.register_column('human_name',
                        default_visible = True,
                        can_sort = False,
                        can_filter_wildcards = False)

        f = ParamFilter()
        f.add_filter('prefix',
                     allow_none = False)

        cls._query_people_filter = f

    def query_people(self, start_row=None,
                           rows_per_page=None,
                           order=-1,
                           sort_col=None,
                           filters = None,
                           **params):

        if not filters:
            filters = {}
        filters = self._query_people_filter.filter(filters, conn=self)
        f = {}
        p = filters.get('prefix','a').lower()
        p.replace('*', '')
        p += '*'
        f['search'] = p
        result = self.call('user/list',
                           params=f)


        people = result[1]['people']
        return (len(people), people[start_row:rows_per_page + start_row])

    @classmethod
    def register_query_usermemberships(cls):
        path = cls.register_query(
                      'query_usermemberships',
                      cls.query_usermemberships,
                      primary_key_col = 'id',
                      default_sort_col = 'name',
                      default_sort_order = -1,
                      can_paginate = True)

        path.register_column('id',
                        default_visible = False,
                        can_sort = False,
                        can_filter_wildcards = False)
        path.register_column('name',
                        default_visible = True,
                        can_sort = False,
                        can_filter_wildcards = False)
        path.register_column('display_name',
                        default_visible = True,
                        can_sort = False,
                        can_filter_wildcards = False)
        path.register_column('group_type',
                        default_visible = True,
                        can_sort = False,
                        can_filter_wildcards = False)
        path.register_column('irc_channel',
                        default_visible = True,
                        can_sort = False,
                        can_filter_wildcards = False)
        path.register_column('irc_network',
                        default_visible = True,
                        can_sort = False,
                        can_filter_wildcards = False)
        path.register_column('joinmsg',
                        default_visible = True,
                        can_sort = False,
                        can_filter_wildcards = False)
        path.register_column('mailing_list',
                        default_visible = True,
                        can_sort = False,
                        can_filter_wildcards = False)
        path.register_column('mailing_list_url',
                        default_visible = True,
                        can_sort = False,
                        can_filter_wildcards = False)
        path.register_column('needs_sponsor',
                        default_visible = True,
                        can_sort = False,
                        can_filter_wildcards = False)
        path.register_column('owner_id',
                        default_visible = True,
                        can_sort = False,
                        can_filter_wildcards = False)
        path.register_column('prerequisite_id',
                        default_visible = True,
                        can_sort = False,
                        can_filter_wildcards = False),
        path.register_column('url',
                        default_visible = True,
                        can_sort = False,
                        can_filter_wildcards = False)
        path.register_column('user_can_remove',
                        default_visible = True,
                        can_sort = False,
                        can_filter_wildcards = False)
        path.register_column('apply_rules',
                        default_visible = True,
                        can_sort = False,
                        can_filter_wildcards = False)
        path.register_column('creation',
                        default_visible = True,
                        can_sort = False,
                        can_filter_wildcards = False)

        f = ParamFilter()
        f.add_filter('username',['u', 'user', 'name'], allow_none = False)
        f.add_filter('profile',[], allow_none=True)
        f.add_filter('show_approved',['approved', 'a'], allow_none = True)
        f.add_filter('show_unapproved',['unapproved', 'un'], allow_none = True)
        cls._query_usermemberships_filter = f

    @classmethod
    def register_query_userinfo(cls):
        path = cls.register_query(
                      'query_userinfo',
                      cls.query_userinfo,
                      can_paginate = False)

        f = ParamFilter()
        f.add_filter('username',['u', 'user', 'name'], allow_none = False)
        f.add_filter('profile',[], allow_none=True)
        cls._query_userinfo_filter = f

    def query_userinfo(self, start_row=None,
                             rows_per_page=None,
                             order=-1,
                             sort_col=None,
                             filters = {},
                             **params):

        filters = self._query_userinfo_filter.filter(filters)

        un = filters.get('username')
        profile = filters.get('profile', False)

        current_id = self._environ.get('repoze.who.identity')

        current_user = None
        if current_id:
            current_user = current_id['repoze.who.userid']
            if profile:
                un = current_user

        if un == current_user:
            view = current_id['person']
        else:
            view = self.get_user_view(un)
            if 'error_type' in view:
                return (-1, view)

        if not view:
            return None

        created = DateTimeDisplay(view['creation'])
        if created.datetime:
            view['created_display'] = created.datetime.strftime("%d %b %Y")
        else:
            view['created_display'] = ''

        # there is only ever one row returned
        return (1, [view])

    def query_usermemberships(self, start_row=None,
                                    rows_per_page=None,
                                    order=-1,
                                    sort_col=None,
                                    filters = {},
                                    **params):

        filters = self._query_usermemberships_filter.filter(filters)

        un = filters.get('username')
        sa = filters.get('show_approved', True)
        sun = filters.get('show_unapproved', True)
        profile = filters.get('profile', False)

        current_id = self._environ.get('repoze.who.identity')

        current_user = None
        if current_id:
            current_user = current_id['repoze.who.userid']
            if profile:
                un = current_user

        count = 0
        rows = []

        if un == current_user:
            info = current_id['person']
        else:
            info = self.get_user_view(un)

        if info:
            if sa:
                rows.extend(info['approved_memberships'])
            if sun:
                rows.extend(info['unapproved_memberships'])

            count = len(rows)
            last_index = 0
            if start_row + rows_per_page >= count:
                last_index = count - 1
            else:
                last_index = start_row + rows_per_page

            rows = rows[start_row:last_index]

        return (count, rows)

    def group_membership_over_time(self, group_name="cla_done"):
        # This is the magic time (in microseconds since the UNIX Epoch) that
        # Toshio gave me where the end of the initial FAS2 import lies. Any
        # timestamps prior to this can't be trusted.
        # start_date = "2008-03-12 02:06:00"
        start_date = 1205305560000

        fas = self.create_fas_object()

        group = fas.people_query(constraints={'group': group_name,
                                              'role_status': 'approved'},
                                 columns=['role_approval'])
        approval = {}

        for row in group:
            if row['role_approval'] == None:
                continue
            timeobject = DateTimeDisplay(row['role_approval'].split('+')[0])
            timetuple = timeobject.datetime.timetuple()
            timetuple_new = (timetuple.tm_year, timetuple.tm_mon,
                             timetuple.tm_mday, 0, 0, 0, 0, 0, 0)
            timestamp = int(time.mktime(timetuple_new))*1000
            if timestamp in approval.keys():
                approval[timestamp] += 1
            else:
                approval[timestamp] = 1

        approval_times = approval.keys()
        approval_times.sort()

        data = []
        approves = 0
        for thattime in approval_times:
            approves += approval[thattime]
            if thattime > start_date:
                data.append((thattime, approves))

        return data
