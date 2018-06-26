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

import requests

from fedoracommunity.connectors.api import \
    IConnector, IQuery, ParamFilter

class FafConnector(IConnector, IQuery):
    _method_paths = {}
    _query_paths = {}
    _cache_prompts = {}

    # IConnector
    @classmethod
    def register(cls):
        cls.register_query_problems()

    #IQuery
    @classmethod
    def register_query_problems(cls):
        path = cls.register_query(
            'query_problems',
            cls.query_problems,
            cache_prompt=None,
            primary_key_col='id',
            default_sort_col='count',
            default_sort_order=-1,
            can_paginate=True)

        path.register_column(
            'id',
            default_visible=True,
            can_sort=True,
            can_filter_wildcards=False)

        path.register_column(
            'status',
            default_visible=True,
            can_sort=True,
            can_filter_wildcards=False)

        path.register_column(
            'crash_function',
            default_visible=True,
            can_sort=True,
            can_filter_wildcards=True)

        path.register_column(
            'count',
            default_visible=True,
            can_sort=True,
            can_filter_wildcards=False)

        f = ParamFilter()
        f.add_filter('package', ['p'], allow_none=True)
        f.add_filter('status', ['s'], allow_none=True)
        f.add_filter('crash_function', ['c'], allow_none=True)
        cls._query_builds_filter = f

    def query_problems(self, start_row=None,
                       rows_per_page=10,
                       order=-1,
                       sort_col=None,
                       filters=None,
                       **params):

        if not filters:
            filters = {}
        filters = self._query_builds_filter.filter(filters, conn=self)

        package = filters.get('package', '')

        url = "https://retrace.fedoraproject.org/faf/problems/?component_names=" + package
        headers = {'Accept': 'application/json'}

        response = requests.get(url, headers=headers)

        if response.status_code == requests.codes['ok']:
            problems = response.json()['problems']

        return (len(problems), problems)
