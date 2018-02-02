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

from fedoracommunity.connectors.api import IConnector, ICall, IQuery
from tg import config
from fedoracommunity.search import utils

import urllib
import xapian

try:
    import json
except ImportError:
    import simplejson as json


class XapianConnector(IConnector, ICall, IQuery):
    _method_paths = {}
    _query_paths = {}
    _cache_prompts = {}

    def __init__(self, environ=None, request=None):
        super(XapianConnector, self).__init__(environ, request)
        self._search_db = xapian.Database(
            config.get('fedoracommunity.connector.xapian.package-search.db',
                       'xapian/search'))

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
                      cache_prompt=None,  # This means "don't cache".
                      primary_key_col='name',
                      default_sort_col='name',
                      default_sort_order=-1,
                      can_paginate=True)

        path.register_column('name',
                             default_visible=True,
                             can_sort=False,
                             can_filter_wildcards=False)

        path.register_column('summary',
                             default_visible=True,
                             can_sort=False,
                             can_filter_wildcards=False)

    def search_packages(self, start_row=None,
                        rows_per_page=None,
                        order=-1,
                        sort_col=None,
                        filters={},
                        **params):

        search_string = filters.get('search')
        # short circut for empty string
        if not search_string:
            return (0, [])

        search_string = urllib.unquote_plus(search_string)

        search_string = utils.filter_search_string(search_string)
        phrase = '"%s"' % search_string

        # add exact matchs
        search_terms = search_string.split(' ')
        search_terms = [t.strip() for t in search_terms if t.strip()]
        for term in search_terms:
            search_string += " EX__%s__EX" % term

        # add phrase match
        search_string += " OR %s" % phrase

        if len(search_terms) > 1:
            # add near phrase match (phrases that are near each other)
            search_string += " OR (%s)" % ' NEAR '.join(search_terms)

        # Add partial/wildcard matches
        search_string += " OR (%s)" % ' OR '.join([
            "*%s*" % term for term in search_terms])

        matches = self.do_search(search_string,
                                 start_row,
                                 rows_per_page,
                                 order,
                                 sort_col)

        count = matches.get_matches_estimated()
        rows = []
        for m in matches:
            result = json.loads(m.document.get_data())

            if 'link' not in result:
                result['link'] = result['name']

            for pkg in result['sub_pkgs']:
                if 'link' not in pkg:
                    pkg['link'] = pkg['name']

            rows.append(result)

        return (count, rows)

    def get_package_info(self, package_name):
        search_name = utils.filter_search_string(package_name)
        search_string = "%s EX__%s__EX" % (search_name, search_name)

        matches = self.do_search(search_string, 0, 10)
        if len(matches) == 0:
            return None

        # Sometimes (rarely), the first match is not the one we actually want.
        for match in matches:
            result = json.loads(match.document.get_data())
            if result['name'] == package_name:
                return result
            if any([sp['name'] == package_name for sp in result['sub_pkgs']]):
                return result

        return None

    def do_search(self,
                  search_string,
                  start_row=None,
                  rows_per_page=None,
                  order=-1,
                  sort_col=None):
        enquire = xapian.Enquire(self._search_db)
        qp = xapian.QueryParser()
        qp.set_database(self._search_db)
        flags = xapian.QueryParser.FLAG_DEFAULT | \
            xapian.QueryParser.FLAG_PARTIAL | \
            xapian.QueryParser.FLAG_WILDCARD
        query = qp.parse_query(search_string, flags)

        enquire.set_query(query)
        matches = enquire.get_mset(start_row, rows_per_page)

        return matches
