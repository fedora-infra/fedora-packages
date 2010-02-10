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

import os
import sys
import yum

class YumConnector(IConnector, ICall, ISearch, IQuery):
    _method_paths = {}
    _query_paths = {}

    def __init__(self, environ=None, request=None):
        super(YumConnector, self).__init__(environ, request)
        self._yum_client = yum.YumBase()
        self._yum_client.doConfigSetup(fn = self._conf_file)

    # IConnector
    @classmethod
    def register(cls):
        cls._conf_file = config.get('fedoracommunity.connector.yum.conf',
                                   '/etc/yum/yum.conf')

        cls.register_search_packages()

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

        search = self._yum_client.searchGenerator(searchlist, search_term, showdups = False)
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
                row['parent_pkg'] = parent_pkg
                row['is_subpkg'] = (parent_pkg != pkg.name)

                results.append(row)
                seen.add(pkg.name)

        self._yum_client.close()
        return results
