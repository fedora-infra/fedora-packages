from paste.deploy.converters import asbool
from pylons import config
from fedora.client import ProxyClient
from beaker.cache import Cache
from datetime import datetime, timedelta

from moksha.connector import IConnector, ICall, IQuery, ParamFilter
from moksha.connector.utils import DateTimeDisplay

bodhi_cache = Cache('bodhi_cache')

class BodhiConnector(IConnector, ICall, IQuery):
    def __init__(self, environ, request):
        super(BodhiConnector, self).__init__(environ, request)
        self._bodhi_client = ProxyClient(self._base_url,
                                         session_as_cookie=False,
                                         insecure = self._insecure)

    # IConnector
    @classmethod
    def register(cls):
        cls._base_url = config.get('fedoracommunity.connector.bodhi.baseurl',
                                   'https://admin.fedoraproject.org/updates')

        check_certs = asbool(config.get('fedora.clients.check_certs', True))
        cls._insecure = not check_certs

        cls.register_query_updates()

    def request_data(self, resource_path, params, _cookies):
        auth_params={}

        fas_info = self._environ.get('FAS_LOGIN_INFO')
        if fas_info:
            session_id = fas_info[0]
            auth_params={'session_id': session_id}

        return self._bodhi_client.send_request(resource_path,
                                               req_params=params,
                                               auth_params=auth_params)

    def introspect(self):
        # FIXME: return introspection data
        return None

    #ICall
    def call(self, resource_path, params, _cookies=None):
        # proxy client only returns structured data so we can pass
        # this off to request_data but we should fix that in ProxyClient
        return self.request_data(resource_path, params, _cookies)

    #IQuery

    @classmethod
    def register_query_updates(cls):
        path = cls.register_query(
                      'query_updates',
                      cls.query_updates,
                      primary_key_col = 'request_id',
                      default_sort_col = 'request_id',
                      default_sort_order = -1,
                      can_paginate = True)

        path.register_column('request_id',
                        default_visible = False,
                        can_sort = False,
                        can_filter_wildcards = False)
        path.register_column('updateid',
                        default_visible = True,
                        can_sort = False,
                        can_filter_wildcards = False)
        path.register_column('nvr',
                        default_visible = True,
                        can_sort = False,
                        can_filter_wildcards = False)
        path.register_column('submitter',
                        default_visible = True,
                        can_sort = False,
                        can_filter_wildcards = False)
        path.register_column('status',
                        default_visible = True,
                        can_sort = False,
                        can_filter_wildcards = False)
        path.register_column('request',
                        default_visible = True,
                        can_sort = False,
                        can_filter_wildcards = False)
        path.register_column('karma',
                        default_visible = True,
                        can_sort = False,
                        can_filter_wildcards = False)
        path.register_column('nagged',
                        default_visible = True,
                        can_sort = False,
                        can_filter_wildcards = False)
        path.register_column('type',
                        default_visible = True,
                        can_sort = False,
                        can_filter_wildcards = False)
        path.register_column('approved',
                        default_visible = True,
                        can_sort = False,
                     can_filter_wildcards = False)
        path.register_column('date_submitted',
                        default_visible = True,
                        can_sort = False,
                        can_filter_wildcards = False)
        path.register_column('date_pushed',
                        default_visible = True,
                        can_sort = False,
                        can_filter_wildcards = False)
        path.register_column('date_modified',
                        default_visible = True,
                        can_sort = False,
                        can_filter_wildcards = False)
        path.register_column('comments',
                        default_visible = True,
                        can_sort = False,
                        can_filter_wildcards = False)
        path.register_column('bugs',
                        default_visible = True,
                        can_sort = False,
                        can_filter_wildcards = False)
        path.register_column('builds',
                        default_visible = True,
                        can_sort = False,
                        can_filter_wildcards = False)
        path.register_column('releases',
                        default_visible = True,
                        can_sort = False,
                        can_filter_wildcards = False)
        path.register_column('release',
                        default_visible = True,
                        can_sort = False,
                        can_filter_wildcards = False)
        path.register_column('karma_level',
                        default_visible = True,
                        can_sort = False,
                        can_filter_wildcards = False)

        def _profile_user(conn, filter_dict, key, value, allow_none):
            if value:
                user = None
                ident = conn._environ.get('repoze.who.identity')
                if ident:
                    user = ident.get('repoze.who.userid')
                if user or allow_none:
                    filter_dict['username'] = user

        f = ParamFilter()
        f.add_filter('package', ['nvr'], allow_none=False)
        f.add_filter('user',['u', 'username', 'name'], allow_none = False)
        f.add_filter('profile',[], allow_none=False,
                     filter_func=_profile_user,
                     cast=bool)
        f.add_filter('status',['status'], allow_none = True)
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

        params.update(filters)
        params['tg_paginate_no'] = int(start_row/rows_per_page)

        # Ask for twice as many updates.  This is so we can handle the case
        # where there are two updates for each package, one for each release.
        # Yes, worst case we get twice as much data as we ask for, but this
        # allows us to do *much* more efficient database calls on the server.
        params['tg_paginate_limit'] = rows_per_page * 2

        results = self._bodhi_client.send_request('list', req_params=params)

        total_count = results[1]['num_items']
        updates_list = self._group_updates(results[1]['updates'],
                                           num_packages=rows_per_page)

        for up in updates_list:
            versions = []
            releases = []

            for dist_update in up['dist_updates']:
                versions.append(dist_update['version'])
                releases.append(dist_update['release_name'])

            up['name'] = up['package_name']
            # FIXME: Don't embed HTML, just send it as a list and have the
            #        template handle it
            up['versions'] = '<br/>'.join(versions)
            up['releases'] = '<br/>'.join(releases)
            up['status'] = up['dist_updates'][0]['status']

            # fix this...
            up['nvr'] = up['dist_updates'][0]['title']
            up['request_id'] = up['nvr']

            actions = []

            # Right now we're making the assumption that if you're logged
            # in, we query by your username, thus you should be able to
            # modify these updates.  This way, we avoid the pkgdb calls.
            # Ideally, we should get the real ACLs from the pkgdb connector's
            # cache.
            if filters.get('username'):
                # If we have multiple updates that are all in the same state,
                # then create a single set of action buttons to control all
                # of them.  If not,then supply separate ones.
                if len(up['dist_updates']) > 1:
                    if up['dist_updates'][0]['status'] != \
                       up['dist_updates'][1]['status']:
                        for update in up['dist_updates']:
                            for action in self._get_update_actions(update):
                                actions.append(action)
                    else:
                        for update in up['dist_updates']:
                            for action in self._get_update_actions(update):
                                actions.append(action)
                else:
                    # Create a single set of action buttons
                    update = up['dist_updates'][0]
                    for action in self._get_update_actions(update):
                        actions.append(action)

            up['actions'] = ''
            for action in actions:
                reqs = ''
                for u in up['dist_updates']:
                    reqs += "update_action('%s', '%s');" % (u['title'], action[0])

                # FIXME: Don't embed HTML
                up['actions'] += """
                    <a href="#" id="%s_%s" onclick="%s return false;">%s</a><br/>
                    """ % (up['dist_updates'][0]['title'].replace('.', ''),
                           action[0], reqs, action[1])

            #dates
            dp = up['dist_updates'][0]['date_pushed']
            ds = up['dist_updates'][0]['date_submitted']

            dtd = DateTimeDisplay(ds)
            ds_when = dtd.when(0)
            dp_when = None
            elapsed = dtd.time_elapsed(0)
            if dp:
                dtd = DateTimeDisplay(ds, dp)
                dp_when = dtd.when(1)
                elapsed = dtd.time_elapsed(0, 1)
            up['date_pushed_display'] = dp_when
            up['date_submitted_display'] = ds_when
            up['elapsed_display'] = elapsed

            # karma
            # FIXME: take into account karma from both updates
            k = up['dist_updates'][0]['karma']
            if k:
                up['karma_str'] = "%+d"%k
            else:
                up['karma_str'] = " %d"%k
            up['karma_level'] = 'meh'
            if k > 0:
                up['karma_level'] = 'good'
            if k < 0:
                up['karma_level'] = 'bad'

        return (total_count, updates_list)

    def _get_update_actions(self, update):
        actions = []
        if update['status'] == 'testing':
            actions.append(('unpush', 'Unpush'))
            actions.append(('stable', 'Push to stable'))
        if update['status'] == 'pending':
            actions.append(('testing', 'Push to testing'))
            actions.append(('stable', 'Push to stable'))
        if update['request']:
            actions.append(('revoke', 'Cancel push'))
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
                pkg = build['package']['name']
                if pkg not in packages:
                    if num_packages and i >= num_packages:
                        done = True
                        break
                    packages[pkg] = {
                            'package_name' : pkg,
                            'dist_updates': []
                            }
                    i += 1
                else:
                    skip = False
                    for up in packages[pkg]['dist_updates']:
                        if up['release_name'] == update['release']['long_name']:
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

        result = [packages[pkg] for pkg in packages]

        sort_col = 'date_submitted'
        if result[0]['dist_updates'][0]['status'] == 'stable':
            sort_col = 'date_pushed'

        result = sorted(result, reverse=True, cmp=lambda x, y:
                     cmp(x['dist_updates'][0][sort_col],
                         y['dist_updates'][0][sort_col]))

        return result

    def get_releases(self):
        return bodhi_cache.get_value(key='releases', expiretime=86400,
                                     createfunc=self._get_releases)

    def _get_releases(self):
        return self._bodhi_client.send_request('get_releases')[1]['releases']

    def get_dashboard_stats(self, username=None):
        return bodhi_cache.get_value(key='dashboard_%s' % username,
                createfunc=lambda: self._get_dashboard_stats(username),
                expiretime=300)

    def _get_dashboard_stats(self, username):
        options = {}
        results = {}

        if username:
            options['username'] = username

        for status in ('pending', 'testing'):
            options['status'] = status
            results[status] = self.query_updates_count(**options)['count']

        now = datetime.utcnow()
        options['status'] = 'stable'
        options['after'] = week_start = now - timedelta(weeks=1)
        results['stable'] = self.query_updates_count(**options)['count']

        return results

    def query_updates_count(self, status, username=None,
                            before=None, after=None):
        # FIXME; this won't cache properly, as the datetimes has miliseconds..
        return bodhi_cache.get_value(key='count_%s_%s_%s_%s' % (
                status, username, before, after), expiretime=300,
                createfunc=lambda: self._query_updates_count(status, username,
                                                             before, after))

    def _query_updates_count(self, status, username, before, after):
        params = {'count_only': True}
        label = status + ' updates pushed'

        if username:
            params['username'] = username
        if status:
            params['status'] = status
        if before:
            before = str(before)
            params['end_date'] = before.split('.')[0]
        if after:
            after = str(after)
            params['start_date'] = after.split('.')[0]

        count = self.call('list', params)[1]['num_items']

        return {'count': count, 'label': label, 'state': status}
