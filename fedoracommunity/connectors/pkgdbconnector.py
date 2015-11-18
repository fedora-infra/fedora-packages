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

from fedoracommunity.connectors.api import IConnector, ICall, IQuery, ParamFilter, ISearch
from tg import config
import pkgdb2client
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
    _cache_prompts = {}

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

    def introspect(self):
        # FIXME: return introspection data
        return None

    #ICall
    def call(self, resource_path, params=None, _cookies=None):
        raise NotImplementedError()

    def request_collection_table(self, eol=False):
        session_id = None
        if self._environ:
            identity = self._environ.get('repoze.who.identity')
            if identity:
                session_id = identity.get('session_id')

        table = {}
        pkgdb = pkgdb2client.PkgDB(self._base_url)
        if not eol:
            active = ['Active', 'Under Development']
            co = pkgdb.get_collections(clt_status=active)
        else:
            co = pkgdb.get_collections()

        for c in co['collections']:
            table[c['branchname']] = c

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
            if dist['collection']['koji_name'] == 'rawhide':
                d = dist
                break

        p = d['package']
        result['name'] = p['name']
        result['description'] = p['description']
        result['summary'] = p['summary']
        result['owner'] = d.get('owner', None)

        return result

    def get_fedora_releases(self, rawhide=True):
        return pkgdb_cache.get_value(key='fedora_releases_%s' % rawhide,
                createfunc=lambda : self._get_fedora_releases(rawhide),
                type="memory", expiretime=COLLECTION_TABLE_CACHE_TIMEOUT)

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
                releases.append((collection['gitbranchname'], '%s %s' % (
                        name, version),collection['koji_name']))
        releases.sort(cmp=lambda x, y: cmp(int(x[1].split()[-1]),
                                           int(y[1].split()[-1])), reverse=True)
        if rawhide:
            releases = [('master', 'Rawhide', 'rawhide')] + releases
        return releases

    def get_pkgdb(self):
        return pkgdb2client.PkgDB(self._base_url)

    def get_num_pkgs_per_collection(self, name='Fedora'):
        """ Get the number of packages per collection in a flot-friendly format """
        data = []
        rawhide = None
        options = {'xaxis': {'ticks': []},
                  'series': {'lines': {'show': True},
                             'points': {'show': True}},
                  'grid': {'hoverable': True, 'clickable': True}}

        collections = self.get_pkgdb().get_collections()
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
