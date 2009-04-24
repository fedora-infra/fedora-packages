import time

from datetime import datetime, timedelta
from pylons import config
from bugzilla import Bugzilla
from beaker.cache import Cache

from moksha.connector import IConnector, ICall, IQuery, ParamFilter
from moksha.connector.utils import DateTimeDisplay

bugzilla_cache = Cache('bugzilla_cache')

class BugzillaConnector(IConnector, ICall, IQuery):
    _method_paths = {}
    _query_paths = {}

    def __init__(self, environ=None, request=None):
        super(BugzillaConnector, self).__init__(environ, request)
        self._bugzilla = Bugzilla(url=self._base_url)

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
        cls._query_bugs_filter = f

    def query_bug_stats(self, *args, **kw):
        package = kw.get('package', None)
        if not package:
            raise Exception('No package specified')
        return bugzilla_cache.get_value(key=package, expiretime=21600,
                           createfunc=lambda: self._get_bug_stats(package))

    def _get_bug_stats(self, package, collection='Fedora'):
        """
        Returns (# of open bugs, # of new bugs, # of closed bugs)
        """
        results = {}
        last_week = str(datetime.utcnow() - timedelta(days=7)),

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

    def query_bugs(self, start_row=None, rows_per_page=10, order=-1,
                   sort_col='number', filters=None, **params):
        if not filters:
            filters = {}
        filters = self._query_bugs_filter.filter(filters, conn=self)
        collection = filters.get('collection', 'Fedora')
        package = filters['package']
        query = {
                'product': collection,
                'component': package,
                'bug_status': ['NEW', 'ASSIGNED', 'REOPENED'],
                'order': 'bug_id',
                }
        results = self._bugzilla.query(query)
        total_count = len(results)
        bugids = [bug.bug_id for bug in results][start_row:start_row+rows_per_page]
        bugs = self._bugzilla.getbugs(bugids)

        bugs_list = []

        for bug in bugs:
            modified = datetime(*time.strptime(str(bug.last_change_time),
                                               '%Y%m%dT%H:%M:%S')[:-2])
            bugs_list.append({
                'id': bug.bug_id,
                'status': bug.bug_status.title(),
                'description': bug.summary,
                'last_modified': DateTimeDisplay(modified).when(0)['when'],
                'release': '%s %s' % (collection, bug.version),
                })

        return (total_count, bugs_list)
