# This file is part of Fedora Community.
# Copyright (C) 2008-2014  Red Hat, Inc.
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

from fedoracommunity.connectors.api import (
    IConnector,
    ICall,
    IQuery,
    ParamFilter,
    ISearch,
)

from tg import config
from urllib import quote

import lockfile
import os
import sys
import yum
import re


class YumConnector(IConnector, ICall, ISearch, IQuery):
    _method_paths = {}
    _query_paths = {}
    fedora_base_repo_re = re.compile('Fedora ([0-9]+)$')

    def __init__(self, environ=None, request=None):
        super(YumConnector, self).__init__(environ, request)
        self._yum_client = yum.YumBase()

        yumlock_file = config.get('yumlock', os.getcwd() + "/yumlock")
        self.yumlock = lockfile.FileLock(yumlock_file)

        with self.yumlock:
            self._yum_client.doConfigSetup(
                fn=self._conf_file,
                root=os.getcwd(),
            )

    # IConnector
    @classmethod
    def register(cls):
        cls._conf_file = config.get('fedoracommunity.connector.yum.conf',
                                    'production/yum.conf')

        cls.register_search_packages()
        cls.register_query_provides()
        cls.register_query_requires()
        cls.register_query_required_by()
        cls.register_query_conflicts()
        cls.register_query_obsoletes()

        cls.register_method('get_file_tree', cls.call_get_file_tree)

    def introspect(self):
        # FIXME: return introspection data
        return None

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

        path.register_column('description',
                             default_visible = True,
                             can_sort = False,
                             can_filter_wildcards = False)

        path.register_column('sourcerpm',
                             default_visible = True,
                             can_sort = False,
                             can_filter_wildcards = False)


        # cache the column names so we don't have to edit them in two places
        cls._package_search_field_list = []
        for col in path['columns']:
            cls._package_search_field_list.append(col)

    def search_packages(self, search_term):
        searchlist = self._package_search_field_list

        search_term = search_term.split()

        with self.yumlock:
            search = self._yum_client.searchGenerator(
                searchlist, search_term, showdups=False)

        results = []
        seen = set()
        for (pkg, values) in search:
            if pkg.name not in seen:
                row = {}
                for s in searchlist:
                    row[s] = pkg.__getattribute__(s)

                # get the parent package from the source rpm name
                # and compare it to the package name to see if this is a
                # sub package
                parent_pkg = pkg.sourcerpm.rsplit('-', 2)[0]
                row['parent_pkg'] = quote(parent_pkg)
                row['is_subpkg'] = (parent_pkg != pkg.name)

                results.append(row)
                seen.add(pkg.name)

        with self.yumlock:
            self._yum_client.close()

        return results

    def _setup_repo(self, repo, arch):
        repo_id = repo.lower().replace(' ', '-')

        arch_id = arch
        # there are no noarch repos so we need to enable the x86_64 repo
        if arch_id == 'noarch':
           arch_id = 'x86_64'

        enable_repos = ["%s-%s" % (repo_id, arch_id)]
        # enable base id if this is a testing repo
        if repo_id.endswith('-testing'):
            repo_id = repo_id[:-8]
            enable_repos.append("%s-%s" % (repo_id, arch_id))

        if self.fedora_base_repo_re.match(repo) is not None:
            # latest package for fedora repo can be in either the base repo
            # or the updates repo so treat as one repo and enable both
            enable_repos.append('%s-updates-%s' % (repo_id, arch_id))

        # enable repos we care about
        with self.yumlock:
            for r in self._yum_client.repos.findRepos('*'):
                if r.id in enable_repos:
                    r.enable()
                else:
                    r.disable()

    def _get_required_by(self, package, repo, arch):
        self._setup_repo(repo, arch)
        with self.yumlock:
            pkgs = self._yum_client.pkgSack.getRequires(package)
        return pkgs

    def _get_pkg_object(self, package, repo, arch):
        self._setup_repo(repo, arch)

        with self.yumlock:
            try:
                pkg = self._yum_client.getPackageObject(
                    (package, arch, None, None, None))
            except yum.Errors.DepError:
                # might be a noarch subpackage so try again
                # FIXME: we should list individual subpackages with archs in
                # latest build db
                pkg = self._yum_client.getPackageObject(
                    (package, 'noarch', None, None, None))

        return pkg

    def _pkgtuples_to_rows(self,
                           pkgtuples,
                           _eq='=',
                           _gt='>', _lt='<',
                           _ge='>=', _le='<=',
                           find_provided_by=False):

        rows = []

        for pkg in pkgtuples:
            flags =  pkg[1]
            ops = None
            version = ''
            if flags == "EQ":
                ops = _eq
            elif flags == "GT":
                ops = _gt
            elif flags == "LT":
                ops = _lt
            elif flags == "GE":
                ops = _ge
            elif flags == "LE":
                ops = _le

            ver_tuple = pkg[2]
            for i in xrange(len(ver_tuple)):
                if ver_tuple[i] is None:
                    break;

                if i > 0:
                    version += '-'
                version += ver_tuple[i]

            provided_by = None
            if find_provided_by:

                with self.yumlock:
                    p = [pkg[0]]
                    provided_by_pkg = self._yum_client.searchPackageProvides(p)

                if len(provided_by_pkg) > 0:
                    provided_by = tuple(set(map(
                        lambda p: p.name,
                        provided_by_pkg.keys()
                    )))

            rows.append({'name': pkg[0],
                         'version': version,
                         'flags': flags,
                         'ops': ops,
                         'provided_by': provided_by})
        return rows

    @classmethod
    def register_query_provides(cls):
        path = cls.register_query(
                      'query_provides',
                      cls.query_provides,
                      primary_key_col = 'name',
                      default_sort_col = 'name',
                      default_sort_order = -1,
                      can_paginate = True)

        path.register_column('name',
                        default_visible = True,
                        can_sort = True,
                        can_filter_wildcards = False)

        path.register_column('flags',
                        default_visible = False,
                        can_sort = False,
                        can_filter_wildcards = False)

        path.register_column('version',
                        default_visible = True,
                        can_sort = False,
                        can_filter_wildcards = False)
        path.register_column('ops',
                        default_visible = True,
                        can_sort = False,
                        can_filter_wildcards = False)

        f = ParamFilter()
        f.add_filter('package',[], allow_none = False)
        f.add_filter('version',[], allow_none = False)
        f.add_filter('repo',[], allow_none = False)
        f.add_filter('arch',[], allow_none = False)
        cls._query_provides_filter = f

    def query_provides(self, start_row=None,
                            rows_per_page=10,
                            order=-1,
                            sort_col=None,
                            filters=None,
                            **params):

        if not filters:
            filters = {}
        filters = self._query_provides_filter.filter(filters, conn=self)

        package = filters.get('package', '')
        version = filters.get('version', '')
        repo = filters.get('repo', '')
        arch = filters.get('arch', '')

        pkg = self._get_pkg_object(package, repo, arch)

        rows = self._pkgtuples_to_rows(pkg.provides, _eq=None)

        return (len(rows), rows[start_row:start_row + rows_per_page])

    @classmethod
    def register_query_requires(cls):
        path = cls.register_query(
                      'query_requires',
                      cls.query_requires,
                      primary_key_col = 'name',
                      default_sort_col = 'name',
                      default_sort_order = -1,
                      can_paginate = True)

        path.register_column('name',
                        default_visible = True,
                        can_sort = True,
                        can_filter_wildcards = False)

        path.register_column('flags',
                        default_visible = False,
                        can_sort = False,
                        can_filter_wildcards = False)

        path.register_column('version',
                        default_visible = True,
                        can_sort = False,
                        can_filter_wildcards = False)
        path.register_column('ops',
                        default_visible = True,
                        can_sort = False,
                        can_filter_wildcards = False)

        f = ParamFilter()
        f.add_filter('package',[], allow_none = False)
        f.add_filter('version',[], allow_none = False)
        f.add_filter('repo',[], allow_none = False)
        f.add_filter('arch',[], allow_none = False)
        cls._query_requires_filter = f

    def query_requires(self, start_row=None,
                            rows_per_page=10,
                            order=-1,
                            sort_col=None,
                            filters=None,
                            **params):

        if not filters:
            filters = {}
        filters = self._query_requires_filter.filter(filters, conn=self)

        package = filters.get('package', '')
        version = filters.get('version', '')
        repo = filters.get('repo', '')
        arch = filters.get('arch', '')

        pkg = self._get_pkg_object(package, repo, arch)

        rows = self._pkgtuples_to_rows(pkg.requires, find_provided_by=True)

        return (len(rows), rows[start_row:start_row + rows_per_page])

    @classmethod
    def register_query_obsoletes(cls):
        path = cls.register_query(
                      'query_obsoletes',
                      cls.query_obsoletes,
                      primary_key_col = 'name',
                      default_sort_col = 'name',
                      default_sort_order = -1,
                      can_paginate = True)

        path.register_column('name',
                        default_visible = True,
                        can_sort = True,
                        can_filter_wildcards = False)

        path.register_column('flags',
                        default_visible = False,
                        can_sort = False,
                        can_filter_wildcards = False)

        path.register_column('version',
                        default_visible = True,
                        can_sort = False,
                        can_filter_wildcards = False)
        path.register_column('ops',
                        default_visible = True,
                        can_sort = False,
                        can_filter_wildcards = False)

        f = ParamFilter()
        f.add_filter('package',[], allow_none = False)
        f.add_filter('version',[], allow_none = False)
        f.add_filter('repo',[], allow_none = False)
        f.add_filter('arch',[], allow_none = False)
        cls._query_obsoletes_filter = f

    @classmethod
    def register_query_required_by(cls):
        path = cls.register_query(
                      'query_required_by',
                      cls.query_required_by,
                      primary_key_col = 'name',
                      default_sort_col = 'name',
                      default_sort_order = -1,
                      can_paginate = True)

        path.register_column('name',
                        default_visible = True,
                        can_sort = True,
                        can_filter_wildcards = False)

        path.register_column('flags',
                        default_visible = False,
                        can_sort = False,
                        can_filter_wildcards = False)

        path.register_column('version',
                        default_visible = True,
                        can_sort = False,
                        can_filter_wildcards = False)
        path.register_column('ops',
                        default_visible = True,
                        can_sort = False,
                        can_filter_wildcards = False)

        f = ParamFilter()
        f.add_filter('package',[], allow_none = False)
        f.add_filter('version',[], allow_none = False)
        f.add_filter('repo',[], allow_none = False)
        f.add_filter('arch',[], allow_none = False)
        cls._query_required_by_filter = f

    def query_required_by(self, start_row=None,
                                rows_per_page=10,
                                order=-1,
                                sort_col=None,
                                filters=None,
                                **params):

        if not filters:
            filters = {}
        filters = self._query_requires_filter.filter(filters, conn=self)

        package = filters.get('package', '')
        version = filters.get('version', '')
        repo = filters.get('repo', '')
        arch = filters.get('arch', '')

        req_by = self._get_required_by(package, repo, arch)
        rows = []
        for pkg in req_by.keys():
            name = pkg['name']
            ver_list = req_by[pkg]
            req = self._pkgtuples_to_rows(ver_list)
            if req:
                req = req[0]
            else:
                req = ''

            rows.append({'name': name,
                         'requires': req})

        return (len(rows), rows[start_row:start_row + rows_per_page])

    @classmethod
    def register_query_obsoletes(cls):
        path = cls.register_query(
                      'query_obsoletes',
                      cls.query_obsoletes,
                      primary_key_col = 'name',
                      default_sort_col = 'name',
                      default_sort_order = -1,
                      can_paginate = True)

        path.register_column('name',
                        default_visible = True,
                        can_sort = True,
                        can_filter_wildcards = False)

        path.register_column('flags',
                        default_visible = False,
                        can_sort = False,
                        can_filter_wildcards = False)

        path.register_column('version',
                        default_visible = True,
                        can_sort = False,
                        can_filter_wildcards = False)
        path.register_column('ops',
                        default_visible = True,
                        can_sort = False,
                        can_filter_wildcards = False)

        f = ParamFilter()
        f.add_filter('package',[], allow_none = False)
        f.add_filter('version',[], allow_none = False)
        f.add_filter('repo',[], allow_none = False)
        f.add_filter('arch',[], allow_none = False)
        cls._query_obsoletes_filter = f

    def query_obsoletes(self, start_row=None,
                            rows_per_page=10,
                            order=-1,
                            sort_col=None,
                            filters=None,
                            **params):

        if not filters:
            filters = {}
        filters = self._query_obsoletes_filter.filter(filters, conn=self)

        package = filters.get('package', '')
        version = filters.get('version', '')
        repo = filters.get('repo', '')
        arch = filters.get('arch', '')

        pkg = self._get_pkg_object(package, repo, arch)

        rows = self._pkgtuples_to_rows(pkg.obsoletes)

        return (len(rows), rows[start_row:start_row + rows_per_page])

    @classmethod
    def register_query_conflicts(cls):
        path = cls.register_query(
                      'query_conflicts',
                      cls.query_conflicts,
                      primary_key_col = 'name',
                      default_sort_col = 'name',
                      default_sort_order = -1,
                      can_paginate = True)

        path.register_column('name',
                        default_visible = True,
                        can_sort = True,
                        can_filter_wildcards = False)

        path.register_column('flags',
                        default_visible = False,
                        can_sort = False,
                        can_filter_wildcards = False)

        path.register_column('version',
                        default_visible = True,
                        can_sort = False,
                        can_filter_wildcards = False)
        path.register_column('ops',
                        default_visible = True,
                        can_sort = False,
                        can_filter_wildcards = False)

        f = ParamFilter()
        f.add_filter('package',[], allow_none = False)
        f.add_filter('version',[], allow_none = False)
        f.add_filter('repo',[], allow_none = False)
        f.add_filter('arch',[], allow_none = False)
        cls._query_conflicts_filter = f

    def query_conflicts(self, start_row=None,
                            rows_per_page=10,
                            order=-1,
                            sort_col=None,
                            filters=None,
                            **params):

        if not filters:
            filters = {}
        filters = self._query_conflicts_filter.filter(filters, conn=self)

        package = filters.get('package', '')
        version = filters.get('version', '')
        repo = filters.get('repo', '')
        arch = filters.get('arch', '')

        pkg = self._get_pkg_object(package, repo, arch)

        rows = self._pkgtuples_to_rows(pkg.conflicts)

        return (len(rows), rows[start_row:start_row + rows_per_page])

    def _add_to_path(self, paths_cache, path, data):
        if path == '':
            path = '/'

        if path in paths_cache:
            dir_info = paths_cache[path]
            if data:
               dir_info['children'].append(data)
            return

        new_data = {
                    'data': {
                          'title': '',
                          'icon': 'jstree-directory'
                       },
                     'state': 'open',
                     'children': []
                   }
        if data:
           new_data['children'].append(data)
        paths_cache[path] = new_data
        (new_path, dir_name) = os.path.split(path)
        new_data['data']['title'] = dir_name
        self._add_to_path(paths_cache, new_path, new_data)

    def _process_files(self, pkg):
        paths_cache = {'/':{'children':[]}}

        for d in pkg.dirlist:
            self._add_to_path(paths_cache, d, None)

        for full_path in pkg.filelist:
            output = {'name': None,
                      'path': None,
                      'display_size': None,
                      'type': 'F',
                      'modestring': '',
                      'linked_to': None,
                      'user': None,
                      'group': None,
                       # jsTree JSON data
                      'data': {
                          'title': '',
                          'icon': 'jstree-file'
                       },
                       'state': 'open',
                      }

            (path, name) = os.path.split(full_path)
            output['name'] = name
            output['path'] = path
            output['data']['title'] = name

            # yum lacks size and file type data
            #output['display_size'] = self._size_to_human_format(size)

            # construct directory structure
            self._add_to_path(paths_cache, path, output)

        return paths_cache['/']['children']

    def call_get_file_tree(self, resource_path=None, _cookies=None, package=None, repo=None, arch=None):
        try:
            try:
                pkg = self._get_pkg_object(package, repo, arch)
            except yum.Errors.DepError:
                return {
                    'error': "This package does not exist in binary form.  "
                    "Like shadows cast on a wall which only appear when an "
                    "observer steps infront of a light source, it is only an "
                    "illusion floating in the ether of the Interwebs.  Move "
                    "along, there is nothing to see here.",
                }

            return self._process_files(pkg)
        except Exception as e:
            return {'error': "Error: %s" % str(e)}
