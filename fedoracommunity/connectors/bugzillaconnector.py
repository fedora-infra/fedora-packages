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

import time

from datetime import datetime, timedelta
from pylons import config, cache
from bugzilla import Bugzilla

from moksha.connector import IConnector, ICall, IQuery, ParamFilter
from moksha.lib.helpers import DateTimeDisplay

class BugzillaConnector(IConnector, ICall, IQuery):
    _method_paths = {}
    _query_paths = {}

    def __init__(self, environ=None, request=None):
        super(BugzillaConnector, self).__init__(environ, request)
        self._bugzilla = None

    # IConnector
    @classmethod
    def register(cls):
        cls._base_url = config.get('fedoracommunity.connector.bugzilla.baseurl',
                                   'https://bugzilla.redhat.com/xmlrpc.cgi')

        cls.register_query_bugs()

        path = cls.register_method('get_bug_stats', cls.query_bug_stats)

    #IQuery
    @classmethod
    def register_query_bugs(cls):
        path = cls.register_query(
                      'query_bugs',
                      cls.query_bugs,
                      primary_key_col='id',
                      default_sort_col='date',
                      default_sort_order=-1,
                      can_paginate=True)

        path.register_column('id',
                        default_visible=True,
                        can_sort=True,
                        can_filter_wildcards=False)

        path.register_column('status',
                        default_visible=True,
                        can_sort=True,
                        can_filter_wildcards=False)

        path.register_column('description',
                        default_visible=True,
                        can_sort=True,
                        can_filter_wildcards=False)

        path.register_column('release',
                        default_visible=True,
                        can_sort=True,
                        can_filter_wildcards=False)

        f = ParamFilter()
        f.add_filter('package', [], allow_none=False)
        f.add_filter('collection', [], allow_none=False)
        f.add_filter('version', [], allow_none=False)
        cls._query_bugs_filter = f

    def query_bug_stats(self, *args, **kw):
        package = kw.get('package', None)
        if not package:
            raise Exception('No package specified')
        bugzilla_cache = cache.get_cache('bugzilla')
        return bugzilla_cache.get_value(key=package, expiretime=21600,
                           createfunc=lambda: self._get_bug_stats(package))

    def _get_bug_stats(self, package, collection='Fedora'):
        """
        Returns (# of open bugs, # of new bugs, # of closed bugs)
        """
        results = {}
        last_week = str(datetime.utcnow() - timedelta(days=7)),
        if not self._bugzilla:
            self._bugzilla = Bugzilla(url=self._base_url)

        # FIXME: For some reason, doing this as multicall doesn't work properly.
        #mc = self._bugzilla._multicall()

        # Open bugs
        results['open'] = len(self._bugzilla.query({
                'product': collection,
                'component': package,
                'bug_status': ['NEW', 'ASSIGNED', 'REOPENED'],
                }))

        # New bugs
        results['new'] = len(self._bugzilla.query({
                'product': collection,
                'component': package,
                'bug_status': ['NEW'],
                }))

        # New bugs this week
        results['new_this_week'] = len(self._bugzilla.query({
                'product': collection,
                'component': package,
                'bug_status': ['NEW'],
                'chfieldfrom': last_week,
                'chfieldto': 'Now',
                }))

        # Closed bugs
        results['closed'] = len(self._bugzilla.query({
                'product': collection,
                'component': package,
                'bug_status': ['CLOSED'],
                }))

        # Closed bugs this week
        results['closed_this_week'] = len(self._bugzilla.query({
                'product': collection,
                'component': package,
                'bug_status': ['CLOSED'],
                'chfieldfrom': last_week,
                'chfieldto': 'Now',
                }))

        return dict(results=results)

    def _is_security_bug(self, bug):
        security = False
        if bug.assigned_to == 'security-response-team@redhat.com':
            security = True
        elif bug.component == 'vulnerability':
            security = True
        elif 'Security' in bug.keywords:
            security = True
        elif bug.alias:
            for alias in bug.alias:
                if alias.startswith('CVE'):
                    security = True
                    break
        return security

    def query_bugs(self, start_row=None, rows_per_page=10, order=-1,
                   sort_col='number', filters=None, **params):
        if not filters:
            filters = {}
        filters = self._query_bugs_filter.filter(filters, conn=self)
        collection = filters.get('collection', 'Fedora')
        version = filters.get('version', '')

        package = filters['package']
        query = {
                'product': collection,
                'version': version,
                'component': package,
                'bug_status': ['NEW', 'ASSIGNED', 'REOPENED'],
                'order': 'bug_id',
                }
        bugzilla_cache = cache.get_cache('bugzilla')
        key = '%s_%s_%s' % (collection, version, package)
        bugs = bugzilla_cache.get_value(key=key, expiretime=900,
                createfunc=lambda: self._query_bugs(query,
                    filters=filters, collection=collection, **params))
        total_count = len(bugs)
        five_pages = rows_per_page * 5
        if start_row < five_pages: # Cache the first 5 pages of every bug grid
            bugs = bugs[:five_pages]
            bugs = bugzilla_cache.get_value(key=key + '_details',
                    expiretime=900, createfunc=lambda: self.get_bugs(
                        bugs, collection=collection))
        bugs = bugs[start_row:start_row+rows_per_page]
        if start_row >= five_pages:
            bugs = self.get_bugs(bugs, collection=collection)
        return (total_count, bugs)

    def _query_bugs(self, query, start_row=None, rows_per_page=10, order=-1,
                   sort_col='number', filters=None, collection='Fedora',
                   **params):
        if not self._bugzilla:
            self._bugzilla = Bugzilla(url=self._base_url)
        results = self._bugzilla.query(query)
        results.reverse()
        return [bug.bug_id for bug in results]

    def get_bugs(self, bugids, collection='Fedora'):
        if not self._bugzilla:
            self._bugzilla = Bugzilla(url=self._base_url)
        bugs = self._bugzilla.getbugs(bugids)
        bugs_list = []
        for bug in bugs:
            modified = DateTimeDisplay(str(bug.last_change_time),
                                       format='%Y%m%dT%H:%M:%S')
            bug_class = ''
            if self._is_security_bug(bug):
                bug_class += 'security-bug '
            bugs_list.append({
                'id': bug.bug_id,
                'status': bug.bug_status.title(),
                'description': bug.summary,
                'last_modified': modified.age(),
                'release': '%s %s' % (collection, bug.version),
                'bug_class': bug_class.strip(),
                })
        return bugs_list
