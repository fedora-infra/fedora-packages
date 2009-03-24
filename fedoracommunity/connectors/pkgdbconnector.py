from moksha.connector import IConnector, ICall, IQuery, ParamFilter, ISearch
from pylons import config
from fedora.client import ProxyClient
from beaker.cache import Cache

COLLECTION_TABLE_CACHE_TIMEOUT= 60 * 60 * 6 # s * m * h = 6 hours
pkgdb_cache = Cache('pkgdb_connector_cache')

class PkgdbConnector(IConnector, ICall, ISearch):
    def __init__(self, environ=None, request=None):
        super(PkgdbConnector, self).__init__(environ, request)
        self._pkgdb_client = ProxyClient(self._base_url,
                                         session_as_cookie=False,
                                         insecure = self._insecure)

    # IConnector
    @classmethod
    def register(cls):
        cls._base_url = config.get('fedoracommunity.connector.pkgdb.baseurl',
                                   'https://admin.fedoraproject.org/pkgdb')

        check_certs = config.get('fedora.clients.check_certs', 'True').lower()
        if check_certs in ('false', '0', 'no'):
            insecure = True
        else:
            # fail safe
            insecure = False

        cls._insecure = insecure

        cls.register_query_userpackages()
        cls.register_query_list_packages()
        cls.register_search_packages()

    def request_data(self, resource_path, params, _cookies):
        return self._pkgdb_client.send_request(resource_path, req_params = params)

    def introspect(self):
        # FIXME: return introspection data
        return None

    #ICall
    def call(self, resource_path, params={}, _cookies=None):
        # proxy client only returns structured data so we can pass
        # this off to request_data but we should fix that in ProxyClient
        return self.request_data(resource_path, params, _cookies)

    def request_collection_table(self):
        table = {}
        co = self.call('/collections')
        for c in co[1]['collections']:
            d = {}
            for i in c:
                d.update(i)

            table[d['id']] = d

        return table

    def get_collection_table(self, invalidate=False):
        # Cache for a long time or if we see a collection
        # that is not in the table

        if invalidate:
            pkgdb_cache.remove_value('_pkgdb_collection_table')

        table = pkgdb_cache.get_value(key='_pkgdb_collection_table',
                                   createfunc=self.request_collection_table,
                                   type="memory",
                                   expiretime=COLLECTION_TABLE_CACHE_TIMEOUT)
        return table

    # ISearch
    @classmethod
    def register_search_packages(cls):
        path = cls.register_search_path(
                      'search_packages',
                      cls.search_packages,
                      primary_key_col = 'name',
                      default_sort_col = 'name',
                      default_sort_order = -1,
                      can_paginate = True)

        path.register_column('name',
                        default_visible = True,
                        can_sort = False,
                        can_filter_wildcards = False)

        path.register_column('summary',
                        default_visible = True,
                        can_sort = False,
                        can_filter_wildcards = False)

    def search_packages(self, search_term):
        result = self.call('search/package',
                           params={'searchwords': search_term,
                                   'tg_paginate_limit':100})
        return result[1]['packages']

    # IQuery
    @classmethod
    def register_query_list_packages(cls):
        path = cls.register_path(
                      'list_packages',
                      cls.query_list_packages,
                      primary_key_col = 'name',
                      default_sort_col = 'name',
                      default_sort_order = -1,
                      can_paginate = True)

        path.register_column('name',
                        default_visible = True,
                        can_sort = False,
                        can_filter_wildcards = False)

        path.register_column('summary',
                        default_visible = True,
                        can_sort = False,
                        can_filter_wildcards = False)

    def query_list_packages(self, start_row=None,
                           rows_per_page=None,
                           order=-1,
                           sort_col=None,
                           filters = {},
                           **params):

        params['tg_paginate_limit'] = rows_per_page
        params['tg_paginate_no'] = int(start_row/rows_per_page)
        params['searchwords'] = ''
        print "fucl"
        results = self._pkgdb_client.send_request('packages', req_params = params)
        total_count = results[1]['pkgCount']
        package_list = results[1]['packages']

        return (total_count, package_list)

    @classmethod
    def register_query_userpackages(cls):
        path = cls.register_path(
                      'query_userpackages',
                      cls.query_userpackages,
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
        path.register_column('summary',
                        default_visible = True,
                        can_sort = False,
                        can_filter_wildcards = False)
        path.register_column('description',
                        default_visible = True,
                        can_sort = False,
                        can_filter_wildcards = False)
        path.register_column('reviewurl',
                        default_visible = False,
                        can_sort = False,
                        can_filter_wildcards = False)
        path.register_column('shouldopen',
                        default_visible = False,
                        can_sort = False,
                        can_filter_wildcards = False)
        path.register_column('statuscode',
                        default_visible = True,
                        can_sort = False,
                        can_filter_wildcards = False)
        path.register_column('collections',
                        default_visible = False,
                        can_sort = False,
                        can_filter_wildcards = False)

        def filter_acls(conn, d, k, v, allow_none):
            acls = []
            if 'acls' in d:
                acls = d['acls']

            acls.append(k)
            d['acls'] = acls

        f = ParamFilter()
        f.add_filter('fasname',['u', 'user', 'name'], allow_none = False)
        f.add_filter('owner', ['o'], cast=bool, allow_none = False, filter_func=filter_acls)
        f.add_filter('maintainer', ['m', 'commit'], cast=bool, allow_none = False, filter_func=filter_acls)
        f.add_filter('approveacls', ['a', 'acls'], cast=bool, allow_none = False, filter_func=filter_acls)
        f.add_filter('watchcommits', ['wc'], cast=bool, allow_none = False, filter_func=filter_acls)
        f.add_filter('watchbugzilla', ['wb', 'bugs'], cast=bool, allow_none = False, filter_func=filter_acls)
        f.add_filter('eol', [], cast=bool)

        cls._query_userpackages_filter = f

    def query_userpackages(self, start_row=None,
                           rows_per_page=None,
                           order=-1,
                           sort_col=None,
                           filters = {},
                           **params):

        filters = self._query_userpackages_filter.filter(filters)

        params.update(filters)
        params['tg_paginate_limit'] = rows_per_page
        params['tg_paginate_no'] = int(start_row/rows_per_page)

        results = self._pkgdb_client.send_request('users/packages', req_params = params)
        total_count = results[1]['pkgCount']
        package_list = results[1]['pkgs']

        co_table = self.get_collection_table()
        for p in package_list:
            p['collections'] = p['listings']
            del p['listings']
            for c in p['collections']:
                id = c['collectionid']
                co_info = co_table.get(id)
                if not co_info:
                    co_table = self.get_collection_table(invalidate=True)
                    co_info = co_table.get(id)

                    # hasn't been updated yet, don't hammer the server
                    if not co_info:
                        c['collectionname'] = 'Not Updated'
                        c['collectionversion'] = ''
                        continue

                c['collectionname'] = co_info['name']
                c['collectionversion'] = co_info['version']

        return (total_count, package_list)