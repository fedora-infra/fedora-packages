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

import ssl
import time
import hashlib

from urllib import urlencode
from datetime import datetime, timedelta
from tg import config
from bugzilla import RHBugzilla3 as Bugzilla

from fedoracommunity.connectors.api import (
    IConnector,
    ICall,
    IQuery,
    ParamFilter,
)
from fedoracommunity.connectors.api.connector import cache_key_generator
from moksha.common.lib.dates import DateTimeDisplay

import dogpile.cache
import threading


# This lets us refresh our cache in a background thread.  Awesome!
def background_runner(mutex, creator):
    def f():
        try:
            creator()
        finally:
            mutex.release()

    t = threading.Thread(target=f)
    t.start()


cache = dogpile.cache.make_region(
    function_key_generator=cache_key_generator,
    key_mangler=lambda key: hashlib.sha1(key).hexdigest(),
    background_runner=background_runner,
)
_cache_configured = False

PRODUCTS = ['Fedora', 'Fedora EPEL']

# Don't query closed bugs for these packages, since the queries timeout
BLACKLIST = ['kernel']

MAX_BZ_QUERIES = 200
BUG_SORT_KEYS = ['status', 'product', 'version', 'bug_id']

OPEN_BUG_STATUS = ['ASSIGNED', 'NEW', 'MODIFIED', 'ON_DEV', 'ON_QA',
                   'VERIFIED', 'FAILS_QA', 'RELEASE_PENDING', 'POST',
                   'REOPENED']


def chunks(l, n):
    """ Yield successive n-sized chunks from l. """
    for i in xrange(0, len(l), n):
        yield l[i:i + n]


class BugzillaConnector(IConnector, ICall, IQuery):
    _method_paths = {}
    _query_paths = {}

    def __init__(self, environ=None, request=None):
        global _cache_configured
        super(BugzillaConnector, self).__init__(environ, request)
        self.__bugzilla = None

        # Defaults for the dogpile cache
        cache_config = {
            "cache.bugzilla.backend": "dogpile.cache.dbm",
            "cache.bugzilla.arguments.filename": "dogpile-cache.dbm",
            "cache.bugzilla.expiration_time": "300",
        }

        cache_config.update(config)

        # Initialize our dogpile cache.
        if not _cache_configured:
            cache.configure_from_config(cache_config, "cache.bugzilla.")
            _cache_configured = True

    @property
    def _bugzilla(self):
        return Bugzilla(url=self._base_url)

    # IConnector
    @classmethod
    def register(cls):
        cls._base_url = config.get(
            'fedoracommunity.connector.bugzilla.baseurl',
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
            'description',
            default_visible=True,
            can_sort=True,
            can_filter_wildcards=False)

        path.register_column(
            'release',
            default_visible=True,
            can_sort=True,
            can_filter_wildcards=False)

        f = ParamFilter()
        f.add_filter('package', [], allow_none=False)
        f.add_filter('collection', [], allow_none=False)
        f.add_filter('version', [], allow_none=False)
        cls._query_bugs_filter = f

    def query_bug_stats(self, path, cookies, package=None, **kw):
        """
        Returns (# of open bugs, # of new bugs, # of closed bugs)

        Registered with the fcomm_connector middleware as get_bug_stats..
        which is non-obvious and confusing.
        """

        if not package:
            raise Exception('No package specified')

        collection = ('Fedora', 'Fedora EPEL')

        queries = ['open', 'blockers', 'new_this_week', 'closed_this_week']

        last_week = str(datetime.utcnow() - timedelta(days=7)),

        # Multi-call support is broken in the latest Bugzilla upgrade
        #mc = self._bugzilla._multicall()

        namespace = str(package) + "-" + str(collection)
        results = []

        # Open bugs - returns an int
        @cache.cache_on_arguments(namespace)
        def open_bugs():
            return len(self._bugzilla.query({
                'product': collection,
                'component': package,
                'status': OPEN_BUG_STATUS,
            }))

        # Blocking Bugs - returns a list of lists of blocked bug ids
        @cache.cache_on_arguments(namespace)
        def blocker_bugs():
            blockers = self._bugzilla.query({
                'product': collection,
                'component': package,
                'status': OPEN_BUG_STATUS,
            })

            return [b.blocks for b in blockers if b.blocks]

        # Closed Bugs this week - returns an int
        @cache.cache_on_arguments(namespace)
        def closed_bugs():
            return len(self._bugzilla.query({
                'product': collection,
                'component': package,
                'status': 'CLOSED',
                'creation_time': last_week,
            }))

        # New bugs this week - returns a list
        @cache.cache_on_arguments(namespace)
        def new_bugs():
            return len(self._bugzilla.query({
                'product': collection,
                'component': package,
                'status': 'NEW',
                'creation_time': last_week,
            }))

        results = [
            open_bugs(),     # int
            blocker_bugs(),  # list of lists of bug_ids
            closed_bugs(),   # int
            new_bugs(),      # int
        ]

        blocks = set()
        # for bug in blocker bugs
        for bug_ids in results[1]:
            map(blocks.add, bug_ids)

        # Generate the URL for the blocker bugs
        args = [
            ('f1', 'blocked'),
            ('o1', 'anywordssubstr'),
            ('classification', 'Fedora'),
            ('query_format', 'advanced'),
            ('component', package),
            ('v1', ' '.join(map(str, blocks))),
        ]

        for product in PRODUCTS:
            args.append(('product', product))

        for status in OPEN_BUG_STATUS:
            args.append(('bug_status', status))

        blocker_url = 'https://bugzilla.redhat.com/buglist.cgi?' + \
            urlencode(args)

        # Convert that list of bug_ids into a list, just like the others
        results[1] = len(results[1])

        results = dict([(q, count) for q, count in zip(queries, results)])

        return dict(results=results, blocker_url=blocker_url)

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
            'bug_status': OPEN_BUG_STATUS,
            #'order': 'bug_id',
        }

        bugs = self._query_bugs(
            query,
            filters=filters,
            collection=collection,
            **params
        )
        total_count = len(bugs)

        # Sort based on feedback from users of bugz.fedoraproject.org/{package}
        # See https://fedorahosted.org/fedoracommunity/ticket/381
        bugs.sort(cmp=bug_sort)
        # Paginate
        bugs = bugs[start_row:start_row + rows_per_page]
        # Get bug details
        bugs = self.get_bugs(bugs, collection=collection)
        return (total_count, bugs)

    @cache.cache_on_arguments()
    def _query_bugs(self, query, start_row=None, rows_per_page=10, order=-1,
                    sort_col='number', filters=None, collection='Fedora',
                    **params):
        """ Make bugzilla queries but only grab up to 200 bugs at a time,
        otherwise we might drop due to SSL timeout.  :/
        """

        results, _results = [], None
        offset, limit = 0, MAX_BZ_QUERIES

        # XXX - This is a hack until the multicall stuff gets worked out
        # https://bugzilla.redhat.com/show_bug.cgi?id=824241 -- threebean
        while _results is None or len(_results):
            query.update(dict(offset=offset, limit=limit))
            _results = self._bugzilla.query(query)
            results.extend(_results)
            offset += limit

        return [
            dict(((key, getattr(bug, key)) for key in BUG_SORT_KEYS))
            for bug in results
        ]

    def get_bugs(self, bugids, collection='Fedora'):

        @cache.cache_on_arguments()
        def _bugids_to_dicts(chunk_of_bugids):

            # First, query bugzilla for ids
            bz_bugs = self._bugzilla.getbugs(chunk_of_bugids)
            dicts = []
            for bug in bz_bugs:
                modified = DateTimeDisplay(str(bug.last_change_time),
                                           format='%Y%m%dT%H:%M:%S')

                bug_class = ''
                if self._is_security_bug(bug):
                    bug_class += 'security-bug '

                d = {
                    'id': bug.bug_id,
                    'status': bug.bug_status.title(),
                    'description': bug.summary,
                    'last_modified': modified.age(),
                    'release': '%s %s' % (collection, bug.version[0]),
                    'bug_class': bug_class.strip(),
                }
                dicts.append(d)

            return dicts

        bugs_list = []

        # XXX - This is a hack until the multicall stuff gets worked out
        # https://bugzilla.redhat.com/show_bug.cgi?id=824241 -- threebean
        for chunk in chunks(bugids, 20):
            chunk_of_bugids = [b['bug_id'] for b in chunk]
            key = 'bug_details_' + ','.join(map(str, chunk_of_bugids))
            bugs_list.extend(_bugids_to_dicts(chunk_of_bugids))

        return bugs_list


def bug_sort(arg1, arg2):
    """ Sort bugs using logic adapted from old pkgdb.

    :author: Ralph Bean <rbean@redhat.com>

    """

    LARGE = 10000

    for key in BUG_SORT_KEYS:
        val1, val2 = arg1[key], arg2[key]

        if key == 'version':
            # version is a string which may contain an integer such as 13 or
            # a string such as 'rawhide'.  We want the integers first in
            # decending order followed by the strings.
            def version_to_int(val):
                try:
                    return -1 * int(val[0])
                except (ValueError, IndexError):
                    return -1 * LARGE

            val1, val2 = version_to_int(val1), version_to_int(val2)
        elif key == 'status':
            # We want items to appear by status in a certain order, not
            # alphabetically.  Items I forgot to hardcode just go last.
            status_order = ['NEW', 'ASSIGNED', 'MODIFIED', 'ON_QA', 'POST']

            def status_to_index(val):
                try:
                    return status_order.index(val)
                except ValueError, e:
                    return len(status_order)

            val1, val2 = status_to_index(val1), status_to_index(val2)

        result = cmp(val1, val2)
        if result:
            return result

    return 0
