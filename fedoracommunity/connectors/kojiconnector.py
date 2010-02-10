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

import re
import koji

from pylons import config, request
from datetime import datetime
from cgi import escape

from moksha.connector import IConnector, ICall, IQuery, ParamFilter
from moksha.api.connectors import get_connector
from moksha.lib.helpers import DateTimeDisplay

class KojiConnector(IConnector, ICall, IQuery):
    _method_paths = {}
    _query_paths = {}

    def __init__(self, environ=None, request=None):
        super(KojiConnector, self).__init__(environ, request)
        self._koji_client = koji.ClientSession(self._base_url)

    # IConnector
    @classmethod
    def register(cls):
        cls._base_url = config.get('fedoracommunity.connector.kojihub.baseurl',
                                   'http://koji.fedoraproject.org/kojihub')

        cls._koji_url = config.get('fedoracommunity.connector.koji.baseurl',
                                   'http://koji.fedoraproject.org/koji')

        cls.register_query_builds()
        cls.register_query_packages()
        cls.register_query_changelogs()

        cls.register_method('get_error_log', cls.call_get_error_log)
        cls.register_method('get_latest_changelog', cls.call_get_latest_changelog)

    def request_data(self, resource_path, params, _cookies):
        return self._koji_client.callMethod(resource_path, **params)

    def introspect(self):
        # FIXME: return introspection data
        return None

    #ICall
    def call(self, resource_path, params, _cookies=None):
        # koji client only returns structured data so we can pass
        # this off to request_data
        return self.request_data(resource_path, params, _cookies)

    def _mock_error_code_to_log_file(self, err_code):
        if err_code == 1:
            log_file = 'build.log'
        elif err_code == 10 or err_code == 30:
            log_file = 'root.log'
        else:
            print "Unhandled error code :", err_code

        return log_file

    def _get_file_url(self, task_id, file_name):
        return self._koji_url + '/getfile' + '?taskID=' + str(task_id) + '&name=' + file_name

    def call_get_latest_changelog(self, resource_path, _cookies=None,
                                  build_id=None, task_id=None, state=None):
        changelogs = None
        build_id = int(build_id)
        task_id = int(task_id)
        state = int(state)

        queryOpts = {'limit': 1, 'offset': 0}

        if state != koji.BUILD_STATES['COMPLETE']:
            srpm_tasks = self.call('listTasks', {
                'opts':{
                    'parent': task_id,
                    'method': 'buildSRPMFromSCM',
                    }})
            if srpm_tasks:
                srpm_task = srpm_tasks[0]
                if srpm_task['state'] == koji.TASK_STATES['CLOSED']:
                    srpm_path = None
                    for output in self.call('listTaskOutput', {
                        'taskID': srpm_task['id'],
                        }):
                        if output.endswith('.src.rpm'):
                            srpm_path = output
                            break
                    if srpm_path:
                        changelogs = self.call('getChangelogEntries', {
                            'taskID':srpm_task['id'],
                            'filepath':srpm_path,
                            'queryOpts': queryOpts,
                            })
        else:
            changelogs = self.call('getChangelogEntries', {
                'buildID':build_id,
                'queryOpts': queryOpts
                })

        if not changelogs:
            changelogs = [{
                'author': '',
                'text': 'No changelogs could be found for this package',
                'date': '',
                }]

        return changelogs[0]


    def call_get_error_log(self, resource_path, _cookies=None, task_id=None):
        results = {'log_url':'', 'log_name':'', 'task_id':''}
        task_id = int(task_id);

        decendents = self.call('getTaskDescendents', {'task_id': task_id})
        for task in decendents.keys():
            task_children = decendents[task]
            for child in task_children:
                if child['state'] == koji.TASK_STATES['FAILED']:
                    child_task_id = child['id']

                    error_code = 0
                    try:
                        # this should throw an error
                        child_result = self.call('getTaskResult', {'taskId': child_task_id})
                    except koji.BuildError, e:
                        error = str(e)
                        r = re.compile('mock exited with status (\d*)')
                        s = r.search(error)
                        error_code = int(s.group(1))

                    child_files = self.call('listTaskOutput', {'taskID': child_task_id})

                    log_file = self._mock_error_code_to_log_file(error_code)

                    if log_file not in child_files:
                        continue

                    log_url = self._get_file_url(child_task_id, log_file)

                    results['log_url'] = log_url
                    results['log_name'] = log_file
                    results['task_id'] = child_task_id

                    # break out of loop since only one task should fail
                    # and the others should be canceled or succeed
                    # of course there is a race condition but first
                    # failure wins in the rare case there are more than one
                    break

        return results

    #IQuery
    @classmethod
    def register_query_changelogs(cls):
        path = cls.register_query(
                      'query_changelogs',
                      cls.query_changelogs,
                      primary_key_col = 'id',
                      default_sort_col = 'date',
                      default_sort_order = -1,
                      can_paginate = True)

        path.register_column('id',
                        default_visible = True,
                        can_sort = True,
                        can_filter_wildcards = False)

        path.register_column('date',
                        default_visible = True,
                        can_sort = True,
                        can_filter_wildcards = False)

        path.register_column('author',
                        default_visible = True,
                        can_sort = True,
                        can_filter_wildcards = False)

        path.register_column('text',
                        default_visible = True,
                        can_sort = True,
                        can_filter_wildcards = False)

        f = ParamFilter()
        f.add_filter('package',[], allow_none = False)
        cls._query_changelogs_filter = f

        cls._changelog_version_extract_re = re.compile('(.*)\W*<(.*)>\W*-?\W*(.*)')

    def query_changelogs(self, start_row=None,
                           rows_per_page=10,
                           order=-1,
                           sort_col=None,
                           filters=None,
                           **params):

        if not filters:
            filters = {}
        filters = self._query_changelogs_filter.filter(filters, conn=self)

        package = filters.get('package', '')

        if order < 0:
            order = '-' + sort_col
        else:
            order = sort_col

        pkg_id = None
        if package:
            pkg_id = self._koji_client.getPackageID(package)

        if not pkg_id:
            return (0, [])

        queryOpts = None

        qo = {}
        if not (start_row == None):
          qo['offset'] = int(start_row)

        if not (rows_per_page == None):
            qo['limit'] = int(rows_per_page)

        if order:
            qo['order'] = order

        if qo:
            queryOpts = qo

        countQueryOpts = {'countOnly': True}

        self._koji_client.multicall = False

        # FIXME: Figure out how to deal with different builds
        #tags = self._koji_client.listTags(package=pkg_id,
        #                                  queryOpts={})

        # ask pkgdb for the collections table
        # pkgdb = get_connector('pkgdb', self._request)
        # collections_table = pkgdb.get_collection_table()

        # get latest version and use that to get the changelog
        builds = self._koji_client.listBuilds(packageID=pkg_id,
                                              queryOpts={'limit': 1,
                                                         'offset': 0,
                                                         'order': '-nvr'})

        build_id = builds[0].get('build_id')
        if not build_id:
            return (0, [])

        self._koji_client.multicall = True
        self._koji_client.getChangelogEntries(buildID=build_id,
                                                queryOpts=countQueryOpts)

        self._koji_client.getChangelogEntries(buildID=build_id,
                                              queryOpts=queryOpts)

        results = self._koji_client.multiCall()

        changelog_list = results[1][0]

        for entry in changelog_list:
            # try to extract a version and e-mail from the authors field
            m = self._changelog_version_extract_re.match(entry['author'])
            if m:
                entry['author'] = escape(m.group(1))
                entry['email'] = m.group(2)
                entry['version'] = m.group(3)
            else:
                entry['author'] = escape(entry['author'])

            # convert the date to a nicer format
            entry['display_date'] = \
                    DateTimeDisplay(entry['date']).datetime.strftime("%d %b %Y")

        total_count = results[0][0]

        self._koji_client.multicall = False

        return (total_count, changelog_list)

    @classmethod
    def register_query_packages(cls):
        path = cls.register_query(
                      'query_packages',
                      cls.query_packages,
                      primary_key_col = 'id',
                      default_sort_col = 'name',
                      default_sort_order = 1,
                      can_paginate = True)

        path.register_column('id',
                        default_visible = True,
                        can_sort = True,
                        can_filter_wildcards = False)

        path.register_column('name',
                        default_visible = True,
                        can_sort = True,
                        can_filter_wildcards = False)

        f = ParamFilter()
        f.add_filter('prefix',[], allow_none = False)
        cls._query_packages_filter = f

    def query_packages(self, start_row=None,
                           rows_per_page=10,
                           order=1,
                           sort_col=None,
                           filters=None,
                           **params):

        if not filters:
            filters = {}
        filters = self._query_packages_filter.filter(filters, conn=self)
        prefix = filters.get('prefix')
        terms = '%'
        if prefix:
            terms = prefix + '%'

        countQueryOpts = {'countOnly': True}

        if order < 0:
            order = '-' + sort_col
        else:
            order = sort_col

        if start_row == None:
            start_row = 0

        queryOpts = None

        qo = {}
        if not (start_row == None):
          qo['offset'] = int(start_row)

        if not (rows_per_page == None):
            qo['limit'] = int(rows_per_page)

        if order:
            qo['order'] = order

        if qo:
            queryOpts = qo


        countQueryOpts = {'countOnly': True}

        self._koji_client.multicall = True
        self._koji_client.search(terms=terms,
                                 type='package',
                                 matchType='glob',
                                 queryOpts=countQueryOpts)

        self._koji_client.search(terms=terms,
                                type='package',
                                matchType='glob',
                                queryOpts=queryOpts)

        results = self._koji_client.multiCall()
        pkgs = results[1][0]
        total_count = results[0][0]

        return (total_count, pkgs)

    @classmethod
    def register_query_builds(cls):
        path = cls.register_query(
                      'query_builds',
                      cls.query_builds,
                      primary_key_col = 'build_id',
                      default_sort_col = 'build_id',
                      default_sort_order = -1,
                      can_paginate = True)

        path.register_column('build_id',
                        default_visible = True,
                        can_sort = True,
                        can_filter_wildcards = False)
        path.register_column('nvr',
                        default_visible = True,
                        can_sort = True,
                        can_filter_wildcards = False)
        path.register_column('owner_name',
                        default_visible = True,
                        can_sort = True,
                        can_filter_wildcards = False)
        path.register_column('state',
                        default_visible = True,
                        can_sort = True,
                        can_filter_wildcards = False)

        def _profile_user(conn, filter_dict, key, value, allow_none):
            d = filter_dict

            if value:
                user = None

                ident = conn._environ.get('repoze.who.identity')
                if ident:
                    user = ident.get('repoze.who.userid')

                if user or allow_none:
                    d['user'] = user

        f = ParamFilter()
        f.add_filter('user',['u', 'username', 'name'], allow_none = False)
        f.add_filter('profile',[], allow_none=False,
                     filter_func=_profile_user,
                     cast=bool)
        f.add_filter('package',['p'], allow_none = True)
        f.add_filter('state',['s'], allow_none = True)
        f.add_filter('query_updates', allow_none=True, cast=bool)
        cls._query_builds_filter = f

    def query_builds(self, start_row=None,
                           rows_per_page=10,
                           order=-1,
                           sort_col=None,
                           filters=None,
                           **params):

        if not filters:
            filters = {}
        filters = self._query_builds_filter.filter(filters, conn=self)

        username = filters.get('user', '')
        package = filters.get('package', '')
        state = filters.get('state')

        complete_before = None
        complete_after = None

        # need a better way to specify this
        # completed_filter = filters.get('completed')
        # if completed_filter:
        #    if completed_filter['op'] in ('>', 'after'):
        #        complete_after = completed_filter['value']
        #    elif completed_filter['op'] in ('<', 'before'):
        #        complete_before = completed_filter['value']

        if order < 0:
            order = '-' + sort_col
        else:
            order = sort_col

        user = self._koji_client.getUser(username)
        
        # we need to check if this user exists
        if username and not user:
            return (0, [])

        id = None
        if user:
            id = user['id']

        pkg_id = None
        if package:
            pkg_id = self._koji_client.getPackageID(package)

        queryOpts = None

        if state:
            state = int(state)

        qo = {}
        if not (start_row == None):
          qo['offset'] = int(start_row)

        if not (rows_per_page == None):
            qo['limit'] = int(rows_per_page)

        if order:
            qo['order'] = order

        if qo:
            queryOpts = qo

        countQueryOpts = {'countOnly': True}

        self._koji_client.multicall = True
        self._koji_client.listBuilds(packageID=pkg_id,
                      userID=id,
                      state=state,
                      completeBefore = complete_before,
                      completeAfter = complete_after,
                      queryOpts=countQueryOpts)

        self._koji_client.listBuilds(packageID=pkg_id,
                      userID=id,
                      state=state,
                      completeBefore = complete_before,
                      completeAfter = complete_after,
                      queryOpts=queryOpts)

        results = self._koji_client.multiCall()
        builds_list = results[1][0]
        total_count = results[0][0]
        for b in builds_list:
            state = b['state']
            b['state_str'] = koji.BUILD_STATES[state].lower()
            start = DateTimeDisplay(b['creation_time'])
            complete = b['completion_time']
            completion_display = None
            if not complete:
                completion_display = {
                        'when': 'In progress...',
                        'should_display_time': False,
                        'time': '',
                        }
                completion_display['elapsed'] = start.age(granularity='minute')
            else:
                completion_display = {}
                complete = DateTimeDisplay(b['completion_time'])
                completion_display['elapsed'] = start.age(complete,
                        granularity='minute')
                completion_display['when'] = complete.age(
                        granularity='minute', general=True) + ' ago'

                ident = request.environ.get('repoze.who.identity')
                if ident:
                    username = ident.get('repoze.who.userid')
                    tz = ident['person']['timezone']
                    completion_display['time'] = \
                            complete.astimezone(tz).strftime('%I:%M %p %Z')
                else:
                    completion_display['time'] = \
                            complete.datetime.strftime('%I:%M %p') + ' UTC'

            b['completion_time_display'] = completion_display

        # Query the bodhi update status for each build
        if filters.get('query_updates'):
            bodhi = get_connector('bodhi')
            bodhi.add_updates_to_builds(builds_list)

        self._koji_client.multicall = False

        return (total_count, builds_list)

