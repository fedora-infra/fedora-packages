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

from moksha.connector import IConnector, ICall, IQuery, ParamFilter
from pylons import config
from urllib import quote

import os
import sys
import xapian 
import cPickle

class XapianConnector(IConnector, ICall, IQuery):
    _method_paths = {}
    _query_paths = {}

    def __init__(self, environ=None, request=None):
        super(XapianConnector, self).__init__(environ, request)
        self._xapian_db = xapian.Database(config.get('fedoracommunity.connector.xapian.db', 'xapian'))

    # IConnector
    @classmethod
    def register(cls):
        cls.register_search_packages()

    def introspect(self):
        # FIXME: return introspection data
        return None

    @classmethod
    def register_search_packages(cls):
        path = cls.register_query(
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

    def search_packages(self, start_row=None,
                              rows_per_page=None,
                              order=-1,
                              sort_col=None,
                              filters = {},
                              **params):

        search_term = filters.get('search');
        enquire = xapian.Enquire(self._xapian_db)
        qp = xapian.QueryParser()
        qp.set_database(self._xapian_db)
        query = qp.parse_query(search_term)

        # FIXME: do validation
        enquire.set_query(query)
        matches = enquire.get_mset(start_row, rows_per_page);

        count = matches.get_matches_estimated()
        rows = []
        for m in matches:
            result = cPickle.loads(m.document.get_data())
            rows.append(result)

        return (count, rows)
