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

from datetime import datetime

import requests

from tg import config
from cgi import escape
from paste.httpexceptions import HTTPBadRequest
from paste.httpexceptions import HTTPBadGateway


from fedoracommunity.connectors.api import \
    IConnector, IQuery, ParamFilter
from fedoracommunity.connectors.api import get_connector
from moksha.common.lib.dates import DateTimeDisplay


class KojiConnector(IConnector, IQuery):
    _method_paths = {}
    _query_paths = {}
    _cache_prompts = {}

    def __init__(self, environ=None, request=None):
        super(KojiConnector, self).__init__(environ, request)
        self._koji_client = koji.ClientSession(self._base_url)

    @classmethod
    def query_builds_cache_prompt(cls, msg):
        if not '.buildsys.build.state.change' in msg['topic']:
            return

        if msg['msg']['instance'] != 'primary':
            return

        # Kill two cache slots.  one for builds of this package in any state
        # and one for builds of this package in this particular state.
        name = msg['msg']['name']
        return [
            {'package': name, 'state': ''}, # '' means 'all'
            {'package': name, 'state': msg['msg']['new']},
        ]

    @classmethod
    def query_changelogs_cache_prompt(cls, msg):
        if not '.mdapi.repo.update' in msg['topic']:
            return

        release = msg['msg']['name']
        table = msg['msg']['differences'].get('changelog', {})
        added = table.get('added', [])
        removed = table.get('removed', [])
        names = set([entry[0] for entry in added + removed])
        for name in names:
            yield {'release': release, 'package_name': name}


    # IConnector
    @classmethod
    def register(cls):
        cls._base_url = config.get('fedoracommunity.connector.kojihub.baseurl',
                                   'http://koji.fedoraproject.org/kojihub')

        cls._koji_url = config.get('fedoracommunity.connector.koji.baseurl',
                                   'http://koji.fedoraproject.org/koji')

        cls._koji_pkg_url = config.get(
            'fedoracommunity.connector.koji.pkgurl',
            'http://koji.fedoraproject.org/packages')

        cls._mdapi_url = config.get('fedoracommunity.connector.mdapi.baseurl',
                                    'https://apps.fedoraproject.org/mdapi')

        cls.register_query_builds()
        cls.register_query_changelogs()

    def introspect(self):
        # FIXME: return introspection data
        return None

    #IQuery
    @classmethod
    def register_query_changelogs(cls):
        path = cls.register_query(
            'query_changelogs',
            cls.query_changelogs,
            cls.query_changelogs_cache_prompt,
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
            'date',
            default_visible=True,
            can_sort=True,
            can_filter_wildcards=False)

        path.register_column(
            'author',
            default_visible=True,
            can_sort=True,
            can_filter_wildcards=False)

        path.register_column(
            'text',
            default_visible=True,
            can_sort=True,
            can_filter_wildcards=False)

        f = ParamFilter()
        f.add_filter('package_name', list(), allow_none=False)
        f.add_filter('release', list(), allow_none=False)
        cls._query_changelogs_filter = f

        cls._changelog_version_extract_re = re.compile(
            '(.*)\W*<(.*)>\W*-?\W*(.*)')

    def query_changelogs(self, start_row=None,
                         rows_per_page=10,
                         order=-1,
                         sort_col=None,
                         filters=None,
                         **params):

        if not filters:
            filters = {}

        if not filters.get('package_name'):
            raise HTTPBadRequest('"package_name" is a required filter.')

        package_name = filters['package_name']
        release = filters.get('release', 'rawhide')

        url = '/'.join([self._mdapi_url, release, 'changelog', package_name])
        response = requests.get(url)
        if not bool(response):
            raise HTTPBadGateway("Failed to talk to mdapi, %r %r" % (
                url, response))

        data = response.json()

        if 'files' in data:
            # This is the *old* way to do it
            data = data['files']
        elif 'changelog' in data:
            # This is the *new* way to do it
            # https://github.com/fedora-infra/mdapi/commit/c2eafd8d05171fdcb3fd699835c0a44e02088724#commitcomment-14646204
            data = data['changelog']
        else:
            # IMPOSSIBLE!
            raise HTTPBadGateway("Got unexpected response from mdapi.")

        for i, entry in enumerate(data):
            entry['text'] = entry['changelog']
            m = self._changelog_version_extract_re.match(entry['author'])
            if m:
                entry['author'] = escape(m.group(1))
                entry['email'] = m.group(2)
                entry['version'] = m.group(3)
            else:
                entry['author'] = escape(entry['author'])

            # convert the date to a nicer format
            obj = DateTimeDisplay(datetime.fromtimestamp(entry['date']))
            entry['display_date'] = obj.datetime.strftime("%d %b %Y")

        return len(data), data

    @classmethod
    def register_query_builds(cls):
        path = cls.register_query(
            'query_builds',
            cls.query_builds,
            cls.query_builds_cache_prompt,
            primary_key_col='build_id',
            default_sort_col='build_id',
            default_sort_order=-1,
            can_paginate=True)

        path.register_column(
            'build_id',
            default_visible=True,
            can_sort=True,
            can_filter_wildcards=False)

        path.register_column(
            'nvr',
            default_visible=True,
            can_sort=True,
            can_filter_wildcards=False)

        path.register_column(
            'owner_name',
            default_visible=True,
            can_sort=True,
            can_filter_wildcards=False)

        path.register_column(
            'state',
            default_visible=True,
            can_sort=True,
            can_filter_wildcards=False)

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
        f.add_filter('user', ['u', 'username', 'name'], allow_none=False)
        f.add_filter('profile', list(), allow_none=False,
                     filter_func=_profile_user,
                     cast=bool)
        f.add_filter('package', ['p'], allow_none=True)
        f.add_filter('state', ['s'], allow_none=True)
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
        if not (start_row is None):
            qo['offset'] = int(start_row)

        if not (rows_per_page is None):
            qo['limit'] = int(rows_per_page)

        if order:
            qo['order'] = order

        if qo:
            queryOpts = qo

        countQueryOpts = {'countOnly': True}

        self._koji_client.multicall = True
        self._koji_client.listBuilds(
            packageID=pkg_id,
            userID=id,
            state=state,
            completeBefore=complete_before,
            completeAfter=complete_after,
            queryOpts=countQueryOpts)

        self._koji_client.listBuilds(
            packageID=pkg_id,
            userID=id,
            state=state,
            completeBefore=complete_before,
            completeAfter=complete_after,
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
                completion_display['elapsed'] = start.age(
                    complete,
                    granularity='minute')
                completion_display['when'] = complete.age(
                    granularity='minute', general=True) + ' ago'

                ident = self._request.environ.get('repoze.who.identity')
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
