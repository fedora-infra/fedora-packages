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

import os
import re
import koji
import rpm

from pylons import config, request
from datetime import datetime
from cgi import escape
from urlgrabber import grabber
from lockfile import LockFile

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

        cls._koji_pkg_url = config.get('fedoracommunity.connector.koji.pkgurl',
                                       'http://koji.fedoraproject.org/packages')

        cls._rpm_cache = config.get('fedoracommunity.rpm_cache',
                                    None)
        if not cls._rpm_cache:
            print "You must specify fedoracommunity.rpm_cache in you .ini file"
            exit(-1)

        cls.register_query_builds()
        cls.register_query_packages()
        cls.register_query_changelogs()
        cls.register_query_provides()
        cls.register_query_requires()
        cls.register_query_conflicts()
        cls.register_query_obsoletes()

        cls.register_method('get_error_log', cls.call_get_error_log)
        cls.register_method('get_latest_changelog', cls.call_get_latest_changelog)
        cls.register_method('get_file_tree', cls.call_get_file_tree)

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

    def _size_to_human_format(self, size):
        suffixes = ['K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y']
        result = size
        for suffix in suffixes:
            result /= 1024.0
            if result < 1024:
                return '{0:.1f} {1}'.format(result, suffix)
        return str(size)

    def _add_to_path(self, path, path_cache, data):
        if path == '':
            path = '/'
        if path in path_cache:
            dir_info = path_cache[path]
            if data:
               dir_info.append(data)
            return

        new_data = []
        if data:
           new_data.append(data)
        path_cache[path] = new_data
        (new_path, dir_name) = os.path.split(path)
        self._add_to_path(new_path, path_cache, {'dirname': dir_name, 'content':new_data})

    def _rpm_list_files(self, file_path):
        fd = os.open(file_path, os.O_RDONLY)
        ts = rpm.TransactionSet()
        h = ts.hdrFromFdno(fd)
        attr_names = []

        os.close(fd)
        fi = h.fiFromHeader()
        file_list = []
        links = {}
        paths = {'/':[]}
        result = {}
        for f in fi:
            """
            input: (full_path, size, mode, mtime, Fflags, rdev, inode, nlink, state, Vflags, user, group, digest)
            output: (name, path, display_size, type, modestring, linked_to, user, group)

                name - name of the file, link or directory
                path - path to file, link or directory
                display_size - size of file in human readable terms (e.g. 15.2K, 3.4M, 6.3G)
                type - 'F', 'L' for file and link respectively. Directory info is discarded.
                       Links and directories are guesses based on size.
                modestring - the mode in human readable string format (e.g. xrwxr-xr-)
                linked_to - guess based on files with the same name
                user - user who owns this file
                group - group who owns this file
            """
            (full_path, size, mode, mtime, Fflags, rdev, inode, nlink, state,
             Vflags, user, group, digest) = f
            output = {'name': None,
                      'path': None,
                      'display_size': None,
                      'type': 'F',
                      'modestring': '',
                      'linked_to': None,
                      'user': user,
                      'group': group}

            (path, name) = os.path.split(full_path)
            output['name'] = name
            output['path'] = path
            output['display_size'] = self._size_to_human_format(size)

            digest = int(digest, 16)
            if digest == 0:
                # could be directory or link based on size
                if size > 1024:
                    # if we are a directory check to see if it exists
                    self._add_to_path(path, paths, None)
                    continue;
                else:
                    output['type'] = 'L'
                    links[name] = output
                    # check to see if the file this links to has been seen
                    for file_info in file_list:
                        if file_info['name'] == name:
                            output['linked_to'] = os.path.join(file_info['path'], name)
                            break;
            else:
                # check to see if we are linked to
                link = links.get(name, None)
                if link and not link['linked_to']:
                    link['linked_to'] = os.path.join(path, name)

                file_list.append(output)

            # construct directory structure
            self._add_to_path(path, paths, output)

        return paths['/']

    def _download_rpm(self, nvr, arch):
        if nvr is None or arch is None:
            raise ValueError("Invalid option passed to connector")

        filename = '%s.%s.rpm' % (nvr, arch)
        file_path = os.path.split(filename)
        if file_path[0] != '':
            raise ValueError("Nvr can not contain path elements")
        if len(arch.split('/')) != 1 or os.path.split(arch)[0] != '':
            raise ValueError("Arch can not contain path elements")

        rpm_file_path = os.path.join(self._rpm_cache, filename)
        if os.path.exists(rpm_file_path):
            return rpm_file_path

        lockfile = LockFile(file_path)
        if lockfile.is_locked():
            # block until the lock is released and then assume other
            # thread was successful
            lockfile.acquire()
            lockfile.release()
            return rpm_file_path

        # acquire the lock and release when done
        lockfile.acquire()
        try:
            info = self.call('getBuild', {'buildInfo': nvr})
            if info is None:
                return {'error': 'No such build (%s)' % filename}

            if not os.path.exists(self._rpm_cache):
                os.mkdir(self._rpm_cache,)

            url = '%s/%s/%s/%s/%s/%s' % (self._koji_pkg_url, info['name'], info['version'], info['release'], arch, filename)

            url_file = grabber.urlopen(url, text=filename)
            out = os.open(rpm_file_path, os.O_WRONLY|os.O_CREAT|os.O_TRUNC, 0666)
            try:
                while 1:
                    buf = url_file.read(4096)
                    if not buf:
                        break
                    os.write(out, buf)
            except Exception as e:
                raise e
            finally:
                os.close(out)
                url_file.close()
        finally:
            lockfile.release()

        return rpm_file_path

    def call_get_file_tree(self, resource_path, _cookies=None, nvr=None, arch=None):
        try:
            rpm_file_path = self._download_rpm(nvr, arch)
            return self._rpm_list_files(rpm_file_path)
        except Exception as e:
            return {'error': "Error: %s" % str(e)}

    def call_get_error_log(self, resource_path, _cookies=None, task_id=None):
        results = {'log_url':'', 'log_name':'', 'task_id':''}
        task_id = int(task_id);

        decendents = self.call('getTaskDescendents', {'task_id': task_id,
        })
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
        f.add_filter('build_id',[], allow_none = False)
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

        build_id = int(filters.get('build_id', None))
        task_id = filters.get('task_id', None)
        state = filters.get('state', None)

        if order < 0:
            order = '-' + sort_col
        else:
            order = sort_col

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

        user = None
        id = None
        if username:
            user = self._koji_client.getUser(username)

            # we need to check if this user exists
            if username and not user:
                return (0, [])

            id = user['id']

        pkg_id = None
        if package:
            pkg_id = self._koji_client.getPackageID(package)

        queryOpts = None

        if state:
            try:
                state = int(state)
            except ValueError:
                state_list = []
                for value in state.split(','):
                    state_list.append(int(value))
                    state = state_list

        elif state == '':
            state = None

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
        f.add_filter('nvr',[], allow_none = False)
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

        nvr = filters.get('nvr', '')
        arch = filters.get('arch', '')

        file_path = self._download_rpm(nvr, arch)
        fd = os.open(file_path, os.O_RDONLY)
        ts = rpm.TransactionSet()
        h = ts.hdrFromFdno(fd)
        os.close(fd)

        provides_names = h[rpm.RPMTAG_PROVIDENAME]
        provides_versions = h[rpm.RPMTAG_PROVIDEVERSION]
        provides_flags = h[rpm.RPMTAG_PROVIDEFLAGS]
        provides_ops = []
        for flags in provides_flags:
            op = ""
            if flags & rpm.RPMSENSE_GREATER:
                op = ">"
            elif flags & rpm.RPMSENSE_LESS:
                op = "<"
            if flags & rpm.RPMSENSE_EQUAL:
                op += "="

            provides_ops.append(op)

        total_rows = len(provides_names)
        rows = []
        for i in range(start_row, start_row + rows_per_page):
            if i >= total_rows:
                break
            rows.append({'name': provides_names[i],
                        'version': provides_versions[i],
                        'flags': provides_flags[i],
                        'ops': provides_ops[i]
                       })
        return (total_rows, rows)

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
        f.add_filter('nvr',[], allow_none = False)
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

        nvr = filters.get('nvr', '')
        arch = filters.get('arch', '')

        file_path = self._download_rpm(nvr, arch)
        fd = os.open(file_path, os.O_RDONLY)
        ts = rpm.TransactionSet()
        h = ts.hdrFromFdno(fd)
        os.close(fd)

        requires_names = h[rpm.RPMTAG_REQUIRENAME]
        requires_versions = h[rpm.RPMTAG_REQUIREVERSION]
        requires_flags = h[rpm.RPMTAG_REQUIREFLAGS]
        requires_ops = []
        for flags in requires_flags:
            op = ""
            if flags & rpm.RPMSENSE_GREATER:
                op = ">"
            elif flags & rpm.RPMSENSE_LESS:
                op = "<"
            if flags & rpm.RPMSENSE_EQUAL:
                if op:
                    op += "="
                else:
                    op = "="
            requires_ops.append(op)

        total_rows = len(requires_names)
        rows = []
        for i in range(start_row, start_row + rows_per_page):
            if i >= total_rows:
                break
            rows.append({'name': requires_names[i],
                        'version': requires_versions[i],
                        'flags': requires_flags[i],
                        'ops': requires_ops[i]
                       })

        return (total_rows, rows)

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
        f.add_filter('nvr',[], allow_none = False)
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

        nvr = filters.get('nvr', '')
        arch = filters.get('arch', '')

        file_path = self._download_rpm(nvr, arch)
        fd = os.open(file_path, os.O_RDONLY)
        ts = rpm.TransactionSet()
        h = ts.hdrFromFdno(fd)
        os.close(fd)

        obsoletes_names = h[rpm.RPMTAG_OBSOLETENAME]
        obsoletes_versions = h[rpm.RPMTAG_OBSOLETEVERSION]
        obsoletes_flags = h[rpm.RPMTAG_OBSOLETEFLAGS]
        obsoletes_ops = []
        for flags in obsoletes_flags:
            op = ""
            if flags & rpm.RPMSENSE_GREATER:
                op = ">"
            elif flags & rpm.RPMSENSE_LESS:
                op = "<"
            if flags & rpm.RPMSENSE_EQUAL:
                if op:
                    op += "="
                else:
                    op = "="
            obsoletes_ops.append(op)

        total_rows = len(obsoletes_names)
        rows = []
        for i in range(start_row, start_row + rows_per_page):
            if i >= total_rows:
                break

            rows.append({'name': obsoletes_names[i],
                        'version': obsoletes_versions[i],
                        'flags': obsoletes_flags[i],
                        'ops': obsoletes_ops[i]
                       })

        return (total_rows, rows)

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
        f.add_filter('nvr',[], allow_none = False)
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

        nvr = filters.get('nvr', '')
        arch = filters.get('arch', '')

        file_path = self._download_rpm(nvr, arch)
        fd = os.open(file_path, os.O_RDONLY)
        ts = rpm.TransactionSet()
        h = ts.hdrFromFdno(fd)
        os.close(fd)

        conflict_names = h[rpm.RPMTAG_CONFLICTNAME]
        conflict_versions = h[rpm.RPMTAG_CONFLICTVERSION]
        conflict_flags = h[rpm.RPMTAG_CONFLICTFLAGS]
        conflict_ops = []
        for flags in conflict_flags:
            op = ""
            if flags & rpm.RPMSENSE_GREATER:
                op = ">"
            elif flags & rpm.RPMSENSE_LESS:
                op = "<"
            if flags & rpm.RPMSENSE_EQUAL:
                if op:
                    op += "="
                else:
                    op = "="
            conflict_ops.append(op)

        total_rows = len(conflict_names)
        rows = []
        for i in range(start_row, start_row + rows_per_page):
            if i >= total_rows:
                break
            rows.append({'name': conflict_names[i],
                        'version': conflict_versions[i],
                        'flags': conflict_flags[i],
                        'ops': conflict_ops[i]
                       })

        return (total_rows, rows)

    def get_tasks_for_builds(self, build_ids=[]):
        results = {}

        if build_ids:
            for id in build_ids:
                self._koji_client.multicall = True
                self._koji_client.getBuild(int(id))

            builds = self._koji_client.multiCall()
            if builds:
                for b in builds:
                    self._koji_client.multicall = True
                    task_id = b[0]['task_id']
                    if task_id:
                        self._koji_client.getTaskDescendents(b[0]['task_id'])

                tasks = self._koji_client.multiCall()
                if tasks:
                    for t, id in zip(tasks, build_ids):
                        results[id] = t[0]

        self._koji_client.multicall = False
        return results
