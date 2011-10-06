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
import cgi

try:
    import json
except ImportError:
    import simplejson as json

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

    def _highlight_str(self, string, term):
        # we are injecting html so url escape the origional string
        # to avoid an html injection attack from the packages themselves
        # string = cgi.escape(string)
        lc_string = string.lower()
        term = term.lower()
        term_len = len(term)
        result = ''

        i = lc_string.find(term, 0)
        start = 0
        while i != -1:
            result += string[start:i] + '<span class="match">'
            start = i + term_len
            result += string[i:start] + '</span>'
            i = lc_string.find(term, start)

        result += string[start:]
        return result

    def _highlight_matches(self, row_data, term):
        row_data['name'] = self._highlight_str(row_data['name'], term);
        row_data['summary'] = self._highlight_str(row_data['summary'], term);
        row_data['description'] = self._highlight_str(row_data['description'], term);
        for pkg in row_data['sub_pkgs']:
            pkg['name'] = self._highlight_str(pkg['name'], term);
            pkg['summary'] = self._highlight_str(pkg['summary'], term);
            pkg['description'] = self._highlight_str(pkg['description'], term);

    def search_packages(self, start_row=None,
                              rows_per_page=None,
                              order=-1,
                              sort_col=None,
                              filters = {},
                              **params):

        search_string = filters.get('search')
        # add exact matchs
        search_terms = search_string.split(' ')
        for term in search_terms:
            search_string += " EX__%s__EX" % term

        enquire = xapian.Enquire(self._xapian_db)
        qp = xapian.QueryParser()
        qp.set_database(self._xapian_db)
        query = qp.parse_query(search_string)

        # FIXME: do validation
        enquire.set_query(query)
        matches = enquire.get_mset(start_row, rows_per_page);

        count = matches.get_matches_estimated()
        rows = []
        for m in matches:
            result = json.loads(m.document.get_data())
            # copy name so we can highlight strings that match the search
            result['link'] = result['name']
            # mark matches in <span class="match">
            for term in search_terms:
                self._highlight_matches(result, term)
 
            rows.append(result)

        return (count, rows)
