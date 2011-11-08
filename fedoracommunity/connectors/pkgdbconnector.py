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

from moksha.connector import IConnector, ICall, IQuery, ParamFilter, ISearch
from pylons import config
from fedora.client import ProxyClient, PackageDB
from beaker.cache import Cache

COLLECTION_TABLE_CACHE_TIMEOUT= 60 * 60 * 6 # s * m * h = 6 hours
BASIC_PACKAGE_DATA_CACHE_TIMEOUT = 60 * 60  # 1 hour

# PackageDB's collection status codes
ACTIVE_STATUS = 1
OBSOLETE_STATUS = 13
APPROVED_STATUS = 3
EOL_STATUS = 9
UNDER_DEVELOPMENT_STATUS = 18

pkgdb_cache = Cache('pkgdb_connector_cache')

class PackageNameError(LookupError):
    pass

class PkgdbConnector(IConnector, ICall, ISearch, IQuery):
    _method_paths = {}
    _query_paths = {}

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
        cls.register_query_acls()
        cls.register_query_owners()

    def request_data(self, resource_path, params, _cookies):
        identity = self._environ.get('repoze.who.identity')
        auth_params={}
        if identity:
            session_id = identity.get('session_id')
            auth_params={'session_id': session_id}

        return self._pkgdb_client.send_request(resource_path,
                                               req_params = params,
                                               auth_params=auth_params)

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

    def request_collection_table(self, eol=False):
        session_id = None
        if self._environ:
            identity = self._environ.get('repoze.who.identity')
            if identity:
                session_id = identity.get('session_id')

        table = {}
        pkgdb = PackageDB(self._base_url, insecure=self._insecure, session_id=session_id)
        co = pkgdb.get_collection_list(eol=eol)
        for c, num in co:
            table[c['id']] = c

        return table

    def get_collection_table(self, invalidate=False, active_only=False):
        # Cache for a long time or if we see a collection
        # that is not in the table
        if invalidate:
            try:
                pkgdb_cache.remove_value('_pkgdb_collection_table')
            except KeyError:
                pass

        return pkgdb_cache.get_value(key='_pkgdb_collection_table_%s' % active_only,
                    createfunc=lambda: self.request_collection_table(not active_only),
                    type="memory",
                    expiretime=COLLECTION_TABLE_CACHE_TIMEOUT)

    def request_package_info(self, package, release = None):

        if not release:
            name = ''
            version = ''
        else:
            (name, version) = release.rsplit(" ", 1)

        co = self.call('/acls/name/', {'packageName': package,
                                          'collectionName': name,
                                          'collectionVersion': version})

        if not co:
            return {}

        if 'message' in co[1]:
            raise PackageNameError(co[1]['message'])

        return co

    def get_basic_package_info(self, package, invalidate=False):
        if invalidate:
            try:
                pkgdb_cache.remove_value('_pkgdb_package_info')
            except KeyError:
                pass

        result = {}
        try:
            info = pkgdb_cache.get_value(key=package,
                                   createfunc=lambda : self.request_package_info(package),
                                   type="memory",
                                   expiretime=BASIC_PACKAGE_DATA_CACHE_TIMEOUT)
        except PackageNameError, e:
            result['error_type'] = e.__class__.__name__
            result['error'] = str(e)

            return result

        # search for the rawhide records or use the first one
        # we should ask pkgdb to mark which record has the most authority
        # e.g. which one would have the most up to date info
        d = info[1]['packageListings'][0]

        for dist in info[1]['packageListings']:
            if dist['collection']['koji_name'] == 'dist-rawhide':
                d = dist
                break

        p = d['package']
        result['name'] = p['name']
        result['description'] = p['description']
        result['summary'] = p['summary']
        result['owner'] = d.get('owner', None)

        return result

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
        result = self.call('search/package/',
                           params={'searchwords': search_term,
                                   'tg_paginate_limit':100})
        return result[1]['packages']

    # IQuery
    @classmethod
    def register_query_owners(cls):
        path = cls.register_query(
                      'owners',
                      cls.query_owners,
                      primary_key_col = 'release',
                      default_sort_col = 'release',
                      default_sort_order = -1,
                      can_paginate = True)

        path.register_column('release',
                        default_visible = True,
                        can_sort = False,
                        can_filter_wildcards = False)

        path.register_column('username',
                        default_visible = True,
                        can_sort = False,
                        can_filter_wildcards = False)
        f = ParamFilter()
        f.add_filter('package',['p', 'pkg'], allow_none = False)

        cls._query_acls_filter = f

    def query_owners(self, start_row=None,
                           rows_per_page=None,
                           order=-1,
                           sort_col=None,
                           filters=None,
                           **params):
        if not filters:
            filters = {}

        filters = self._query_acls_filter.filter(filters)

        package = filters.get('package')

        info = pkgdb_cache.get_value(key=package,
                                   createfunc=lambda : self.request_package_info(package),
                                   type="memory",
                                   expiretime=BASIC_PACKAGE_DATA_CACHE_TIMEOUT)

        err_message = info[1].get('message')
        if err_message:
            return (-1, err_message)

        p = info[1]['packageListings']

        collections = self.get_collection_table(False, active_only=True)
        rows = []

        for i in p:
            id = i['collection']['collectionid']
            print id,'=', collections.get(int(id))
            if not collections.get(int(id)):
                continue

            distname = i['collection']['name']
            distver = i['collection']['version']
            owner = i['owner']

            if distname == 'Fedora' and distver == 'devel':
                # make sure it is first in the sort
                rows.append({'release': 'Rawhide',
                            'owner': owner,
                            'distname': 'Fedora',
                            'version':99999999})
            else:
                rows.append({'release': "%s %s" % (distname, distver),
                            'owner': owner,
                            'version':distver,
                            'distname': distname})


        def sort_by_dist(a, b):
            result = 0
            if a['distname'] == 'Fedora' and b['distname'] != 'Fedora':
                result = 1
            elif  b['distname'] == 'Fedora' and a['distname'] != 'Fedora':
                result = -1
            elif a['distname'] != b['distname']:
                result = cmp(a['distname'], b['distname'])
            else: # a and b distname the same so cmp versions
                result = cmp(int(a['version']), int(b['version']))

            if order < 0:
                return -result
            else:
                return result

        rows.sort(sort_by_dist)
        total_count = len(rows)
        return (total_count, rows)

    @classmethod
    def register_query_acls(cls):
        path = cls.register_query(
                      'acls',
                      cls.query_acls,
                      primary_key_col = 'username',
                      default_sort_col = 'username',
                      default_sort_order = -1,
                      can_paginate = True)

        path.register_column('username',
                        default_visible = True,
                        can_sort = False,
                        can_filter_wildcards = False)

        path.register_column('roles',
                        default_visible = True,
                        can_sort = False,
                        can_filter_wildcards = False)
        f = ParamFilter()
        f.add_filter('package',['p', 'pkg'], allow_none = False)
        f.add_filter('roles', allow_none = True)
        f.add_filter('type', allow_none = False)
        f.add_filter('release', allow_none = False)

        cls._query_acls_filter = f

    def query_acls(self, start_row=None,
                           rows_per_page=None,
                           order=-1,
                           sort_col=None,
                           filters=None,
                           **params):
        if not filters:
            filters = {}

        filters = self._query_acls_filter.filter(filters)

        package = filters.get('package')
        roles = filters.get('roles', ['owner', 'maintainer', 'watcher'])
        type = filters.get('type', 'users')
        release = filters.get('release', 'Fedora devel')

        info = pkgdb_cache.get_value(key=package + release,
                                   createfunc=lambda : self.request_package_info(package,
                                                                                 release),
                                   type="memory",
                                   expiretime=BASIC_PACKAGE_DATA_CACHE_TIMEOUT)

        err_message = info[1].get('message')
        if err_message:
            return (-1, err_message)

        p = info[1]['packageListings']

        entities = {}

        for i in p:
            distname = i['collection']['name']
            distver = i['collection']['version']
            owner = i['owner']

            if distname == 'Fedora' and distver == 'devel':
                distname = 'Rawhide'
                distver = ''

            if type == 'users':
                if 'owner' in roles or 'maintainer' in roles:
                    entities[owner] = {'name': owner, 'roles': ['Owner'],'type': 'user'}

                for person in i['people']:
                    aclorder = person['aclOrder']
                    username = person['username']
                    record = entities.get(username,
                                        {'name': username,
                                         'roles': []})
                    record['type'] = 'user'

                    is_maintainer = (aclorder['commit'] or
                                     aclorder['approveacls'])
                    is_watcher = (aclorder['watchbugzilla'] or
                                  aclorder['watchcommits'])

                    if aclorder['approveacls']:
                        record['roles'].append('ACL Approver')
                    if aclorder['commit']:
                        record['roles'].append('Committer')
                    if aclorder['watchbugzilla']:
                        record['roles'].append('Bug Watcher')
                    if aclorder['watchcommits']:
                        record['roles'].append('Commit Watcher')

                    if is_maintainer and 'maintainer' in roles:
                        entities[username] = record

                    if  is_watcher and 'watcher' in roles:
                        entities[username] = record

            if type == 'groups':
                for group in i['groups']:
                    aclorder = group['aclOrder']
                    name = group['name']
                    record = group.get(name,
                                       {'name': name,
                                        'roles': []})
                    record['type'] = 'group'

                    is_maintainer = (aclorder['commit'] or
                                     aclorder['approveacls'])
                    is_watcher = (aclorder['watchbugzilla'] or
                                  aclorder['watchcommits'])

                    if aclorder['approveacls']:
                        record['roles'].append('ACL Approver')
                    if aclorder['commit']:
                        record['roles'].append('Committer')
                    if aclorder['watchbugzilla']:
                        record['roles'].append('Bug Watcher')
                    if aclorder['watchcommits']:
                        record['roles'].append('Commit Watcher')

                    if is_maintainer and 'maintainer' in roles:
                        entities[name] = record
                    if is_watcher and 'watcher' in roles:
                        entities[name] = record

        def sort_entity_list(a, b):
            if order < 0:
                return cmp(b.get('name',''), a.get('name',''))
            else:
                return cmp(a.get('name',''), b.get('name',''))

        entity_list = entities.values()
        entity_list.sort(sort_entity_list)

        total_count = len(entity_list)
        return (total_count, entity_list)

    @classmethod
    def register_query_list_packages(cls):
        path = cls.register_query(
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
                           filters=None,
                           **params):
        if not filters:
            filters = {}

        params['tg_paginate_limit'] = rows_per_page
        params['tg_paginate_no'] = int(start_row/rows_per_page)
        params['searchwords'] = ''

        results = self.call('packages/', params)
        total_count = results[1]['pkgCount']
        package_list = results[1]['packages']

        return (total_count, package_list)

    @classmethod
    def register_query_userpackages(cls):
        path = cls.register_query(
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
        f.add_filter('fasname',['u', 'user', 'name', 'username'], allow_none = False)
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
                           filters=None,
                           **params):

        if not filters:
            filters = {}

        filters = self._query_userpackages_filter.filter(filters)
        # hack since pkgdb equates 'false' = True
        if filters.get('eol') == False:
            del filters['eol']

        rows_per_page = int(rows_per_page)
        start_row = int(start_row)
        params.update(filters)
        params['tg_paginate_limit'] = rows_per_page
        params['tg_paginate_no'] = int(start_row/rows_per_page) + 1

        results = self.call('users/packages/', params)
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

    def get_fedora_releases(self, rawhide=True):
        return pkgdb_cache.get_value(key='fedora_releases_%s' % rawhide,
                createfunc=lambda : self._get_fedora_releases(rawhide),
                type="memory", expiretime=BASIC_PACKAGE_DATA_CACHE_TIMEOUT)

    def _get_fedora_releases(self, rawhide=True):
        releases = []
        collections = self.get_collection_table(active_only=True)
        for collection in collections.values():
            name = collection['name']
            if name in ('Fedora', 'Fedora EPEL'):
                version = collection['version']
                if version == 'devel':
                    # Assume there is always rawhide...
                    #version = ''
                    #name = 'Rawhide'
                    continue
                releases.append((collection['koji_name'], '%s %s' % (
                        name, version)))
        releases.sort(cmp=lambda x, y: cmp(int(x[1].split()[-1]),
                                           int(y[1].split()[-1])), reverse=True)
        if rawhide:
            releases = [('dist-rawhide', 'Rawhide')] + releases
        return releases

    def get_pkgdb(self):
        return PackageDB(self._base_url, insecure=self._insecure)

    def get_num_pkgs_per_collection(self, name='Fedora'):
        """ Get the number of packages per collection in a flot-friendly format """
        data = []
        rawhide = None
        options = {'xaxis': {'ticks': []},
                  'series': {'lines': {'show': True},
                             'points': {'show': True}},
                  'grid': {'hoverable': True, 'clickable': True}}

        collections = self.get_pkgdb().get_collection_list(eol=True)
        for collection, num_pkgs in collections:
            if collection['name'] == name:
                if collection['version'] == 'devel':
                    rawhide = collection
                    rawhide['num_pkgs'] = num_pkgs
                    continue
                version = int(collection['version'])
                data.append((version, num_pkgs))
                options['xaxis']['ticks'].append((version, str(version)))

        # Append rawhide
        data.sort(cmp=lambda x, y: cmp(x[0], y[0]))
        devel = data[-1][0] + 1
        data.append((devel, rawhide['num_pkgs']))
        options['xaxis']['ticks'].append((devel, str(devel)))
        return dict(data=data, options=options)

    def get_collection_by_koji_name(self, koji_name):
        collections = self.get_collection_table(active_only=True)
        for id, collection in collections.items():
            if collection['koji_name'] == koji_name:
                return collection
