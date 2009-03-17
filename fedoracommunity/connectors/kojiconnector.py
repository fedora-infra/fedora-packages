from moksha.connector import IConnector, ICall, IQuery, ParamFilter
from moksha.connector.utils import DateTimeDisplay
from pylons import config
import koji

class KojiConnector(IConnector, ICall, IQuery):
    def __init__(self, environ=None, request=None):
        super(KojiConnector, self).__init__(environ, request)
        self._koji_client = koji.ClientSession(self._base_url)

    # IConnector
    @classmethod
    def register(cls):
        cls._base_url = config.get('fedoracommunity.connector.kojihub.baseurl',
                                   'http://koji.fedoraproject.org/kojihub')

        cls.register_query_builds()

    def request_data(self, resource_path, params, _cookies):
        return self._koji_client.callMethod(resource_path, **params)

    def introspect(self):
        # FIXME: return introspection data
        return None

    #ICall
    def call(self, resource_path, params, _cookies=None):
        # koji client only returns structured data so we can pass
        # this off to request_data
        return self.request_data(resource_path, params, _cookies)

    #IQuery
    @classmethod
    def register_query_builds(cls):
        path = cls.register_path(
                      'query_builds',
                      cls.query_builds,
                      primary_key_col = 'build_id',
                      default_sort_col = 'build_id',
                      default_sort_order = -1,
                      can_paginate = True)

        path.register_column('build_id',
                        default_visible = True,
                        can_sort = True,
                        can_filter_wildcards = False)
        path.register_column('nvr',
                        default_visible = True,
                        can_sort = True,
                        can_filter_wildcards = False)
        path.register_column('owner_name',
                        default_visible = True,
                        can_sort = True,
                        can_filter_wildcards = False)
        path.register_column('state',
                        default_visible = True,
                        can_sort = True,
                        can_filter_wildcards = False)

        def _profile_user(conn, filter_dict, key, value, allow_none):
            d = filter_dict

            if value:
                user = None

                ident = conn._environ.get('repoze.who.identity')
                if ident:
                    user = ident.get('repoze.who.userid')

                if user or allow_none:
                    d['user'] = user

        f = ParamFilter()
        f.add_filter('user',['u', 'username', 'name'], allow_none = False)
        f.add_filter('profile',[], allow_none=False,
                     filter_func=_profile_user,
                     cast=bool)
        f.add_filter('package',['p'], allow_none = True)
        f.add_filter('state',['s'], allow_none = True)
        cls._query_builds_filter = f

    def query_builds(self, start_row=None,
                           rows_per_page=10,
                           order=-1,
                           sort_col=None,
                           filters = {},
                           **params):

        filters = self._query_builds_filter.filter(filters, conn=self)

        user = filters.get('user', '')
        package = filters.get('package', '')
        state = filters.get('state')

        complete_before = None
        complete_after = None

        # need a better way to specify this
        # completed_filter = filters.get('completed')
        # if completed_filter:
        #    if completed_filter['op'] in ('>', 'after'):
        #        complete_after = completed_filter['value']
        #    elif completed_filter['op'] in ('<', 'before'):
        #        complete_before = completed_filter['value']

        if order < 0:
            order = '-' + sort_col
        else:
            order = sort_col

        user = self._koji_client.getUser(user)

        id = None
        if user:
            id = user['id']

        pkg_id = None
        if package:
            pkg_id = self._koji_client.getPackageID(package)

        queryOpts = None

        if state:
            state = int(state)

        qo = {}
        if not (start_row == None):
          qo['offset'] = int(start_row)

        if not (rows_per_page == None):
            qo['limit'] = int(rows_per_page)

        if order:
            qo['order'] = order

        if qo:
            queryOpts = qo

        countQueryOpts = {'countOnly': True}

        self._koji_client.multicall = True
        self._koji_client.listBuilds(packageID=pkg_id,
                      userID=id,
                      state=state,
                      completeBefore = complete_before,
                      completeAfter = complete_after,
                      queryOpts=countQueryOpts)

        self._koji_client.listBuilds(packageID=pkg_id,
                      userID=id,
                      state=state,
                      completeBefore = complete_before,
                      completeAfter = complete_after,
                      queryOpts=queryOpts)

        results = self._koji_client.multiCall()
        builds_list = results[1][0]
        total_count = results[0][0]
        for b in builds_list:
            start = b['creation_time']
            complete = b['completion_time']
            completion_display = None
            if not complete:
                dtd = DateTimeDisplay(start)
                completion_display = {'when': 'In progress...',
                                    'should_display_time': False,
                                    'time': ''}
                elapsed = dtd.time_elapsed(0)
                completion_display['elapsed'] = elapsed['display']
            else:
                dtd = DateTimeDisplay(start, complete)
                completion_display = dtd.when(1)
                elapsed = dtd.time_elapsed(0,1)
                completion_display['elapsed'] = elapsed['display']

            b['completion_time_display'] = completion_display

        self._koji_client.multicall = False

        return (total_count, builds_list)
