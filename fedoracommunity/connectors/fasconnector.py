from moksha.connector import IConnector, ICall, IQuery, ISearch, ParamFilter
from pylons import config
from fedora.client import ProxyClient
from beaker.cache import Cache
from moksha.connector.utils import DateTimeDisplay

USERINFO_CACHE_TIMEOUT= 60 * 5 # s * m = 5 minutes
fas_cache = Cache('fas_connector_cache')

class FasConnector(IConnector, ICall, ISearch, IQuery):
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
        fas_info = self._environ.get('FAS_LOGIN_INFO')

        auth_params={}
        if fas_info:
            session_id = fas_info[0]
            auth_params={'session_id': session_id}

        return self._fas_client.send_request(resource_path,
                                             auth_params = auth_params,
                                             req_params = params)

    def introspect(self):
        # FIXME: return introspection data
        return None

    #ICall
    def call(self, resource_path, params={}, _cookies=None):
        # proxy client only returns structured data so we can pass
        # this off to request_data but we should fix that in ProxyClient
        return self.request_data(resource_path, params, _cookies)

    def request_user_view(self, user):
        view = self.call('user/view', {'username': user});
        if not view:
            return None

        view = view[1]
        extra = {'cla':view['cla'],
                 'admin':view['admin'],
                 'personal':view['personal']
                 }

        view = view['person']
        view.update(extra)
        return view

    def get_user_view(self, user, invalidate=False):
        if not isinstance(user, basestring):
            return None

        key = '_fas_user_info_' + user
        if invalidate:
            fas_cache.remove_value(key)

        info = fas_cache.get_value(key = key ,
                                   createfunc=lambda : self.request_user_view(user),
                                   type="memory",
                                   expiretime=USERINFO_CACHE_TIMEOUT)
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

        path.register_column('username',
                        default_visible = True,
                        can_sort = False,
                        can_filter_wildcards = False)
        path.register_column('human_name',
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
        path = cls.register_path(
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
                           filters = {},
                           **params):

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
        path = cls.register_path(
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
        path = cls.register_path(
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

        if not view:
            return None

        created = DateTimeDisplay(view['creation'])
        created_display = created.when(0)
        if created_display:
            view['created_display'] = created_display['date']
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
