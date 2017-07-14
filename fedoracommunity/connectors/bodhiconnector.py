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

import logging

from itertools import product

from paste.deploy.converters import asbool
from tg import config
from fedora.client.bodhi import Bodhi2Client
from datetime import datetime
from webhelpers.html import HTML

import markdown

from fedoracommunity.connectors.api import get_connector
from fedoracommunity.connectors.api import \
    IConnector, ICall, IQuery, ParamFilter
from moksha.common.lib.dates import DateTimeDisplay

from fedoracommunity.lib.utils import parse_build

log = logging.getLogger(__name__)

koji_build_url = (
    'http://koji.fedoraproject.org/koji/search?'
    'terms=%(name)s-%(version)s-%(release)s&type=build&match=glob')

class BodhiConnector(IConnector, ICall, IQuery):
    _method_paths = dict()
    _query_paths = dict()
    _cache_prompts = dict()

    def __init__(self, environ, request):
        super(BodhiConnector, self).__init__(environ, request)
        self._prod_url = config.get(
            'fedoracommunity.connector.bodhi.produrl',
            'https://bodhi.fedoraproject.org')
        self._bodhi_client = Bodhi2Client(self._base_url,
                                          insecure=self._insecure)

    @classmethod
    def query_updates_cache_prompt(cls, msg):
        if '.bodhi.' not in msg['topic']:
            return

        msg = msg['msg']
        if 'update' in msg:
            update = msg['update']
            release = update['release']['name']
            status = update['status']
            nvrs = [build['nvr'] for build in update['builds']]
            names = ['-'.join(nvr.split('-')[:-2]) for nvr in nvrs]
            releases = [release, '']
            statuses = [status, '']
            groupings = [False]
            headers = ['package', 'release', 'status', 'group_updates']
            combinations = product(names, releases, statuses, groupings)
            for values in combinations:
                yield dict(zip(headers, values))

    @classmethod
    def query_active_releases_cache_prompt(cls, msg):
        if '.bodhi.' not in msg['topic']:
            return

        msg = msg['msg']
        if 'update' in msg:
            nvrs = [build['nvr'] for build in msg['update']['builds']]
            names = ['-'.join(nvr.split('-')[:-2]) for nvr in nvrs]
            for name in names:
                yield {'package': name}

    # IConnector
    @classmethod
    def register(cls):
        cls._base_url = config.get('fedoracommunity.connector.bodhi.baseurl',
                                   'https://bodhi.fedoraproject.org/')

        check_certs = asbool(config.get('fedora.clients.check_certs', True))
        cls._insecure = not check_certs

        cls.register_query_updates()
        cls.register_query_active_releases()

    def request_data(self, path, params):
        return self._bodhi_client.send_request(path, auth=False, params=params)

    def introspect(self):
        # FIXME: return introspection data
        return None

    #ICall
    def call(self, resource_path, params):
        log.debug('BodhiConnector.call(%s)' % locals())
        # proxy client only returns structured data so we can pass
        # this off to request_data but we should fix that in ProxyClient
        return self.request_data(resource_path, params)

    #IQuery
    @classmethod
    def register_query_updates(cls):
        path = cls.register_query(
            'query_updates',
            cls.query_updates,
            cls.query_updates_cache_prompt,
            primary_key_col='request_id',
            default_sort_col='request_id',
            default_sort_order=-1,
            can_paginate=True)

        path.register_column('request_id',
                             default_visible=False,
                             can_sort=False,
                             can_filter_wildcards=False)
        path.register_column('updateid',
                             default_visible=True,
                             can_sort=False,
                             can_filter_wildcards=False)
        path.register_column('nvr',
                             default_visible=True,
                             can_sort=False,
                             can_filter_wildcards=False)
        path.register_column('submitter',
                             default_visible=True,
                             can_sort=False,
                             can_filter_wildcards=False)
        path.register_column('status',
                             default_visible=True,
                             can_sort=False,
                             can_filter_wildcards=False)
        path.register_column('request',
                             default_visible=True,
                             can_sort=False,
                             can_filter_wildcards=False)
        path.register_column('karma',
                             default_visible=True,
                             can_sort=False,
                             can_filter_wildcards=False)
        path.register_column('nagged',
                             default_visible=True,
                             can_sort=False,
                             can_filter_wildcards=False)
        path.register_column('type',
                             default_visible=True,
                             can_sort=False,
                             can_filter_wildcards=False)
        path.register_column('approved',
                             default_visible=True,
                             can_sort=False,
                             can_filter_wildcards=False)
        path.register_column('date_submitted',
                             default_visible=True,
                             can_sort=False,
                             can_filter_wildcards=False)
        path.register_column('date_pushed',
                             default_visible=True,
                             can_sort=False,
                             can_filter_wildcards=False)
        path.register_column('date_modified',
                             default_visible=True,
                             can_sort=False,
                             can_filter_wildcards=False)
        path.register_column('comments',
                             default_visible=True,
                             can_sort=False,
                             can_filter_wildcards=False)
        path.register_column('bugs',
                             default_visible=True,
                             can_sort=False,
                             can_filter_wildcards=False)
        path.register_column('builds',
                             default_visible=True,
                             can_sort=False,
                             can_filter_wildcards=False)
        path.register_column('releases',
                             default_visible=True,
                             can_sort=False,
                             can_filter_wildcards=False)
        path.register_column('release',
                             default_visible=True,
                             can_sort=False,
                             can_filter_wildcards=False)
        path.register_column('karma_level',
                             default_visible=True,
                             can_sort=False,
                             can_filter_wildcards=False)

        f = ParamFilter()
        f.add_filter('package', ['nvr'], allow_none=False)
        f.add_filter('status', ['status'], allow_none=True)
        f.add_filter('group_updates', allow_none=True, cast=bool)
        f.add_filter('granularity', allow_none=True)
        f.add_filter('release', allow_none=False)
        cls._query_updates_filter = f

    def query_updates(self, start_row=None,
                      rows_per_page=None,
                      order=-1,
                      sort_col=None,
                      filters=None,
                      **params):
        if not filters:
            filters = {}

        filters = self._query_updates_filter.filter(filters, conn=self)
        group_updates = filters.get('group_updates', True)

        params.update(filters)
        params['page'] = int(start_row/rows_per_page) + 1

        # If we're grouping updates, ask for twice as much.  This is so we can
        # handle the case where there are two updates for each package, one for
        # each release.  Yes, worst case we get twice as much data as we ask
        # for, but this allows us to do *much* more efficient database calls on
        # the server.
        if group_updates:
            params['rows_per_page'] = rows_per_page * 2
        else:
            params['rows_per_page'] = rows_per_page

        # Convert bodhi1 query format to bodhi2.
        if 'package' in params:
            params['packages'] = params.pop('package')
        if 'release' in params:
            params['releases'] = params.pop('release')

        results = self._bodhi_client.send_request('updates', auth=False, params=params)

        total_count = results['total']

        if group_updates:
            updates_list = self._group_updates(results['updates'],
                                               num_packages=rows_per_page)
        else:
            updates_list = results['updates']

        for up in updates_list:
            versions = []
            releases = []

            if group_updates:
                up['title'] = up['dist_updates'][0]['title']

                for dist_update in up['dist_updates']:
                    versions.append(dist_update['version'])
                    releases.append(dist_update['release_name'])

                up['name'] = up['package_name']

                up['versions'] = versions
                up['releases'] = releases
                up['status'] = up['dist_updates'][0]['status']
                up['nvr'] = up['dist_updates'][0]['title']
                up['request_id'] = up['package_name'] + \
                    dist_update['version'].replace('.', '')
            else:
                chunks = up['title'].split('-')
                up['name'] = '-'.join(chunks[:-2])
                up['version'] = '-'.join(chunks[-2:])
                up['versions'] = chunks[-2]
                up['releases'] = up['release']['long_name']
                up['nvr'] = up['title']
                up['request_id'] = up.get('updateid') or \
                    up['nvr'].replace('.', '').replace(',', '')

            up['id'] = up['nvr'].split(',')[0]

            # A unique id that we can use in HTML class fields.
            #up['request_id'] = up.get('updateid') or \
            #        up['nvr'].replace('.', '').replace(',', '')

            actions = []

            up['actions'] = ''
            for action in actions:
                reqs = ''
                if group_updates:
                    for u in up['dist_updates']:
                        reqs += "update_action('%s', '%s');" % (u['title'],
                                                                action[0])
                    title = up['dist_updates'][0]['title']
                else:
                    reqs += "update_action('%s', '%s');" % (up['title'],
                                                            action[0])
                    title = up['title']

                # FIXME: Don't embed HTML
                up['actions'] += """
                <button id="%s_%s" onclick="%s return false;">%s</button><br/>
                """ % (title.replace('.', ''), action[0], reqs, action[1])

            # Dates
            if group_updates:
                date_submitted = up['dist_updates'][0]['date_submitted']
                date_pushed = up['dist_updates'][0]['date_pushed']
            else:
                date_submitted = up['date_submitted']
                date_pushed = up['date_pushed']

            granularity = filters.get('granularity', 'day')
            ds = DateTimeDisplay(date_submitted)
            up['date_submitted_display'] = ds.age(granularity=granularity,
                                                  general=True) + ' ago'

            if date_pushed:
                dp = DateTimeDisplay(date_pushed)
                up['date_pushed'] = dp.datetime.strftime('%d %b %Y')
                up['date_pushed_display'] = dp.age(granularity=granularity,
                                                   general=True) + ' ago'

            # karma
            # FIXME: take into account karma from both updates
            if group_updates:
                k = up['dist_updates'][0]['karma']
            else:
                k = up['karma']
            if k:
                up['karma_str'] = "%+d" % k
            else:
                up['karma_str'] = " %d" % k
            up['karma_level'] = 'meh'
            if k > 0:
                up['karma_level'] = 'good'
            if k < 0:
                up['karma_level'] = 'bad'

            up['details'] = self._get_update_details(up)

        return (total_count, updates_list)

    def _get_update_details(self, update):
        details = ''
        if update['status'] == 'stable':
            if update.get('updateid'):
                details += HTML.tag('a', c=update['updateid'], href='%s/updates/%s' % (
                                    self._prod_url, update['alias']))
            if update.get('date_pushed'):
                details += HTML.tag('br') + update['date_pushed']
            else:
                details += 'In process...'
        elif update['status'] == 'pending' and update.get('request'):
            details += 'Pending push to %s' % update['request']
            details += HTML.tag('br')
            details += HTML.tag('a', c="View update details >",
                                href="%s/updates/%s" % (self._prod_url,
                                                update['alias']))
        elif update['status'] == 'obsolete':
            for comment in update['comments']:
                if comment['user']['name'] == 'bodhi':
                    if comment['text'].startswith('This update has been '
                                                  'obsoleted by '):
                        details += markdown.markdown(
                            comment['text'], safe_mode="replace")
        return details

    def _get_update_actions(self, update):
        actions = []
        if update['request']:
            actions.append(('revoke', 'Cancel push'))
        else:
            if update['status'] == 'testing':
                actions.append(('unpush', 'Unpush'))
                actions.append(('stable', 'Push to stable'))
            if update['status'] == 'pending':
                actions.append(('testing', 'Push to testing'))
                actions.append(('stable', 'Push to stable'))
        return actions

    def _group_updates(self, updates, num_packages=None):
        """
        Group a list of updates by release.
        This method allows allows you to limit the number of packages,
        for when we want to display 1 package per row, regardless of how
        many updates there are for it.
        """
        packages = {}
        done = False
        i = 0

        if not updates:
            return []

        for update in updates:
            for build in update['builds']:
                pkg = build['nvr'].rsplit('-', 2)[0]
                if pkg not in packages:
                    if num_packages and i >= num_packages:
                        done = True
                        break
                    packages[pkg] = {
                        'package_name': pkg,
                        'dist_updates': list()
                    }
                    i += 1
                else:
                    skip = False
                    for up in packages[pkg]['dist_updates']:
                        if up['release_name'] == \
                           update['release']['long_name']:
                            skip = True
                            break
                    if skip:
                        break
                packages[pkg]['dist_updates'].append({
                    'release_name': update['release']['long_name'],
                    'version': '-'.join(build['nvr'].split('-')[-2:])
                })
                packages[pkg]['dist_updates'][-1].update(update)
            if done:
                break

        result = [packages[p] for p in packages]

        sort_col = 'date_submitted'
        if result[0]['dist_updates'][0]['status'] == 'stable':
            sort_col = 'date_pushed'

        result = sorted(result, reverse=True,
                        cmp=lambda x, y: cmp(
                            x['dist_updates'][0][sort_col],
                            y['dist_updates'][0][sort_col])
                        )

        return result

    def add_updates_to_builds(self, builds):
        """Update a list of koji builds with the corresponding bodhi updates.

        This method makes a single query to bodhi, asking if it knows about
        any updates for a given list of koji builds.  For builds with existing
        updates, the `update` will be added to it's dictionary.

        Currently it also adds `update_details`, which is HTML for rendering
        the builds update options.  Ideally, this should be done client-side
        in the template (builds/templates/table_widget.mak).

        """
        start = datetime.now()
        updates = self.call('get_updates_from_builds', {
            'builds': ' '.join([b['nvr'] for b in builds])})
        if updates:
            # FIXME: Lets stop changing the upstream APIs by putting the
            # session id as the first element, and the results in the second.
            updates = updates[1]

        for build in builds:
            if build['nvr'] in updates:
                build['update'] = updates[build['nvr']]
                status = build['update']['status']
                details = ''
                # FIXME: ideally, we should just return the update JSON and do
                # this logic client-side in the template when the grid data
                # comes in.
                if status == 'stable':
                    details = 'Pushed to updates'
                elif status == 'testing':
                    details = 'Pushed to updates-testing'
                elif status == 'pending':
                    details = 'Pending push to %s' % build['update']['request']

                details += HTML.tag('br')
                details += HTML.tag('a', c="View update details >",
                                    href="%s/updates/%s" % (self._prod_url,
                                                    build['update']['alias']))
            else:
                details = HTML.tag('a', c='Push to updates >',
                                   href='%s/new?builds.text=%s' % (
                                       self._prod_url, build['nvr']))

            build['update_details'] = details

        log.debug(
            "Queried bodhi for builds in: %s" % (datetime.now() - start))

    @classmethod
    def register_query_active_releases(cls):
        path = cls.register_query('query_active_releases',
                                  cls.query_active_releases,
                                  cls.query_active_releases_cache_prompt,
                                  primary_key_col='release',
                                  default_sort_col='release',
                                  default_sort_order=-1,
                                  can_paginate=True)
        path.register_column('release',
                             default_visible=True,
                             can_sort=False,
                             can_filter_wildcards=False)
        path.register_column('stable_version',
                             default_visible=True,
                             can_sort=False,
                             can_filter_wildcards=False)
        path.register_column('testing_version',
                             default_visible=True,
                             can_sort=False,
                             can_filter_wildcards=False)

        f = ParamFilter()
        f.add_filter('package', ['nvr'], allow_none=False)
        cls._query_active_releases = f

    def query_active_releases(self, filters=None, **params):
        releases = list()
        queries = list()
        # Mapping of tag -> release
        release_tag = dict()
        # List of testing builds to query bodhi for
        testing_builds = list()
        # nvr -> release lookup table
        testing_builds_row = dict()
        if not filters:
            filters = dict()
        filters = self._query_updates_filter.filter(filters, conn=self)
        package = filters.get('package')
        pkgdb = get_connector('pkgdb')
        koji = get_connector('koji')._koji_client
        koji.multicall = True

        # TODO - the list of Fedora releases can be obtained from the Bodhi API, instead of the pkgdb API.
        # See https://bodhi.fedoraproject.org/releases/
        for release in pkgdb.get_fedora_releases():
            tag = release[0]
            name = release[1]
            r = {'release': name, 'stable_version': 'None',
                 'testing_version': 'None'}
            if tag == 'rawhide':
                koji.listTagged(
                    tag, package=package, latest=True, inherit=True)
                queries.append(tag)
                release_tag[tag] = r
            else:
                if 'epel' in tag:
                    stable_tag = tag
                    testing_tag = tag + '-testing'
                else:
                    stable_tag = tag + '-updates'
                    testing_tag = stable_tag + '-testing'
                koji.listTagged(stable_tag, package=package,
                                latest=True, inherit=True)
                queries.append(stable_tag)
                release_tag[stable_tag] = r
                koji.listTagged(testing_tag, package=package, latest=True)
                queries.append(testing_tag)
                release_tag[testing_tag] = r
            releases.append(r)

        results = koji.multiCall()

        for i, result in enumerate(results):
            if isinstance(result, dict):
                if 'faultString' in result:
                    log.error("FAULT: %s" % result['faultString'])
                else:
                    log.error("Can't find fault string in result: %s" % result)
            else:
                query = queries[i]
                row = release_tag[query]
                release = result[0]

                if query == 'dist-rawhide':
                    if release:
                        nvr = parse_build(release[0]['nvr'])
                        row['stable_version'] = HTML.tag(
                            'a',
                            c='%(version)s-%(release)s' % nvr,
                            href=koji_build_url % nvr)
                    else:
                        row['stable_version'] = \
                            'No builds tagged with %s' % tag
                    row['testing_version'] = HTML.tag('i', c='Not Applicable')
                    continue
                if release:
                    release = release[0]
                    if query.endswith('-testing'):
                        nvr = parse_build(release['nvr'])
                        row['testing_version'] = HTML.tag(
                            'a',
                            c='%(version)s-%(release)s' % nvr,
                            href=koji_build_url % nvr)
                        testing_builds.append(release['nvr'])
                        testing_builds_row[release['nvr']] = row
                    else:
                        # stable
                        nvr = parse_build(release['nvr'])
                        row['stable_version'] = HTML.tag(
                            'a',
                            c='%(version)s-%(release)s' % nvr,
                            href=koji_build_url % nvr)
                        if release['tag_name'].endswith('-updates'):
                            row['stable_version'] +=  ' (' + HTML.tag(
                                'a', c='update',
                                href='%s/updates/?builds=%s' % (
                                    self._prod_url, nvr['nvr']
                                )
                            ) + ')'

        # If there are updates in testing, then query bodhi with a single call
        if testing_builds:
            data = self.call('updates', {
                'builds': ' '.join(testing_builds)
            })
            updates = data['updates']
            for up in updates:

                for build in up['builds']:
                    if build['nvr'] in testing_builds:
                        break
                else:
                    continue
                build = build['nvr']

                if up.karma > 1:
                    up.karma_icon = 'good'
                elif up.karma < 0:
                    up.karma_icon = 'bad'
                else:
                    up.karma_icon = 'meh'
                karma_ico_16 = '/images/16_karma-%s.png' % up.karma_icon
                karma_icon_url = \
                    self._request.environ.get('SCRIPT_NAME', '') + \
                    karma_ico_16
                karma = 'karma_%s' % up.karma_icon
                row = testing_builds_row[build]
                row['testing_version'] += " " + HTML.tag(
                    'div',
                    c=HTML.tag(
                        'a', href="%s/updates/%s" % (
                            self._prod_url, up.alias),
                        c=HTML.tag(
                            'img', src=karma_icon_url) + HTML.tag(
                            'span',
                            c='%s karma' % up.karma)),
                        **{'class': '%s' % karma})

        return (len(releases), releases)
