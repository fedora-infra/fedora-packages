from moksha.connector import IConnector, ICall, IQuery
from pylons import config
from fedora.client import ProxyClient

class BodhiConnector(IConnector, ICall, IQuery):
    def __init__(self):
        self._bodhi_client = ProxyClient(self._base_url,
                                         session_as_cookie=False,
                                         insecure = self._insecure)

    # IConnector
    @classmethod
    def register(cls):
        cls._base_url = config.get('fedoracommunity.connector.bodhi.baseurl',
                                   'https://admin.fedoraproject.org/updates')

        check_certs = config.get('fedora.clients.check_certs', 'True').lower()
        if check_certs in ('false', '0', 'no'):
            insecure = True
        else:
            # fail safe
            insecure = False

        cls._insecure = insecure
        cls.register_query_updates()

    def request_data(self, resource_path, params, _cookies):
        return self._bodhi_client.send_request(resource_path, request_params = params)

    def introspect(self):
        # FIXME: return introspection data
        return None

    #ICall
    def call(self, resource_path, params, _cookies):
        # proxy client only returns structured data so we can pass
        # this off to request_data but we should fix that in ProxyClient
        return self.request_data(resource_path, params, _cookies)

    #IQuery
    def query(self, resource_path, params, _cookies,
              offset = 0,
              num_rows = 10,
              sort_col = None,
              sort_order = -1,
              filters = {}):

        results = None
        r = {
              "total_rows": 0,
              "row_count": 0,
              "offset": 0,
              "rows": None
            }

        if not sort_col:
            sort_col = self.get_default_sort_col(resource_path)

        if resource_path == 'query_updates':
            if params == None:
                params = {}

            (total_rows, rows) = self.query_updates(offset = offset,
                                                   limit = num_rows,
                                                   order = sort_order,
                                                   sort_col = sort_col,
                                                   filters = filters,
                                                   **params)
            r['total_rows'] = total_rows
            r['row_count'] = len(rows)
            if offset:
                r['offset'] = offset
            r['rows'] = rows

            results = r

        return results

    # BodhiConnector
    @classmethod
    def register_query_updates(cls):
        cls.register_path(
                      'query_updates',
                      primary_key_col = 'request_id',
                      default_sort_col = 'request_id',
                      default_sort_order = -1,
                      can_paginate = True)

        cls.register_column('query_updates', 'request_id',
                        default_visible = False,
                        can_sort = False,
                        can_filter_wildcards = False)
        cls.register_column('query_updates', 'updateid',
                        default_visible = True,
                        can_sort = False,
                        can_filter_wildcards = False)
        cls.register_column('query_updates', 'nvr',
                        default_visible = True,
                        can_sort = False,
                        can_filter_wildcards = False)
        cls.register_column('query_updates', 'submitter',
                        default_visible = True,
                        can_sort = False,
                        can_filter_wildcards = False)
        cls.register_column('query_updates', 'status',
                        default_visible = True,
                        can_sort = False,
                        can_filter_wildcards = False)
        cls.register_column('query_updates', 'request',
                        default_visible = True,
                        can_sort = False,
                        can_filter_wildcards = False)
        cls.register_column('query_updates', 'karma',
                        default_visible = True,
                        can_sort = False,
                        can_filter_wildcards = False)
        cls.register_column('query_updates', 'nagged',
                        default_visible = True,
                        can_sort = False,
                        can_filter_wildcards = False)
        cls.register_column('query_updates', 'type',
                        default_visible = True,
                        can_sort = False,
                        can_filter_wildcards = False)
        cls.register_column('query_updates', 'approved',
                        default_visible = True,
                        can_sort = False,
                        can_filter_wildcards = False)
        cls.register_column('query_updates', 'date_submitted',
                        default_visible = True,
                        can_sort = False,
                        can_filter_wildcards = False)
        cls.register_column('query_updates', 'date_pushed',
                        default_visible = True,
                        can_sort = False,
                        can_filter_wildcards = False)
        cls.register_column('query_updates', 'date_modified',
                        default_visible = True,
                        can_sort = False,
                        can_filter_wildcards = False)
        cls.register_column('query_updates', 'comments',
                        default_visible = True,
                        can_sort = False,
                        can_filter_wildcards = False)
        cls.register_column('query_updates', 'bugs',
                        default_visible = True,
                        can_sort = False,
                        can_filter_wildcards = False)
        cls.register_column('query_updates', 'builds',
                        default_visible = True,
                        can_sort = False,
                        can_filter_wildcards = False)
        cls.register_column('query_updates', 'release_label',
                        default_visible = True,
                        can_sort = False,
                        can_filter_wildcards = False)
        cls.register_column('query_updates', 'release',
                        default_visible = True,
                        can_sort = False,
                        can_filter_wildcards = False)
        cls.register_column('query_updates', 'karma_level',
                        default_visible = True,
                        can_sort = False,
                        can_filter_wildcards = False)

    def query_updates(self, offset=None,
                           limit=None,
                           order=-1,
                           sort_col=None,
                           filters = {},
                           **params):

        # FIXME: make filter an object


        # username = filters.get('username')
        # get_auth = filters.get('get_auth')
        # release = filters.get('release')

        package = filters.get('nvr', filters.get('name'))
        if package:
            filters['package'] = package
            if filters.haskey('nvr'):
                del filters['nvr']

            if filters.haskey('name'):
                del filters['name']

        # request = filters.get('request')
        # status = filters.get('status')
        # type_ = filters.get('type')
        # bugs = filters.get('bugs')

        mine = filters.get('mine')
        if isinstance(mine, str):
            c = mine[0].lower()
            if c == 't' or c == 'y':
                filters['mine'] = True
            elif c == 'f' or c == 'n':
                filters['mine'] = False
            else:
                del filters['mine']
        elif mine:
            filters['mine'] = True

        params.update(filters)
        params['tg_paginate_limit'] = limit
        params['tg_paginate_no'] = int(offset/limit)

        results = self._bodhi_client.send_request('list', req_params = params)

        total_count = results[1]['num_items']
        updates_list = results[1]['updates']

        if total_count > 0:
            for up in updates_list:
                # grab the first build package, the rest are dependencies
                nvr = up['builds'][0]['nvr']

                # split the version and name by getting the
                # position of the second to last dash
                version_pos = nvr.rindex('-')
                version_pos = nvr.rindex('-', 0, version_pos - 1)
                name = nvr[:version_pos]
                version_str = nvr[version_pos + 1:]
                vparts = version_str.split('-')
                version = {'version': vparts[0],
                           'release': vparts[1]}
                up['version'] = version
                up['version_str'] = version_str
                up['name'] = name
                up['request_id'] = nvr
                up['nvr'] = nvr
                up['release_label'] = up['release']['long_name']

                k = up['karma']

                if k:
                    up['karma_str'] = "%+d"%k
                else:
                    up['karma_str'] = " %d"%k

                up['karma_level'] = 'meh'
                if k > 0:
                    up['karma_level'] = 'good'
                if k < 0:
                    up['karma_level'] = 'bad'


        return (total_count, updates_list)