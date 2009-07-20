# This file is part of Fedora Community.
# Copyright (C) 2008-2009  Red Hat, Inc.
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

from tg import expose, tmpl_context, validate
from pylons import cache, request
from formencode import validators
from datetime import datetime, timedelta

from moksha.lib.base import Controller
from moksha.api.widgets import ContextAwareWidget
from moksha.api.connectors import get_connector

class AlertsContainer(ContextAwareWidget):
    template = 'mako:fedoracommunity.mokshaapps.alerts.templates.alertscontainer'

    def update_params(self, d):
        super(AlertsContainer, self).update_params(d)

        # FIXME: Alerts need to be dynamic but for right now
        #        we will have it query directly and cache the results
        c = cache.get_cache('fedoracommunity_alerts_global')

        users = []
        alerts = []

        profile_userid = None
        creds = request.environ.get('repoze.what.credentials')
        if creds and creds.get('repoze.what.userid'):
            profile_userid = creds.get('repoze.what.userid')

        userid = d.get('userid', d.get('user'))

        if userid or profile_userid:
            my_alerts = []
            label = 'Your Packages'
            if d.get('profile'): # if we specify profile this has precedence
                userid = profile_userid
            elif userid: # if we specify userid then use that
                label = '%s\'s Packages' % userid
            else: # else we default to the profile when logged in
                userid = profile_userid

            # Cache for 5 minutes
            users_today = c.get_value(key=userid + '_today',
                 createfunc=lambda : self.get_todays_user_entries(userid),
                 expiretime=300)

            # Cache for a day
            users_this_week = c.get_value(key=userid + '_this_week',
                 createfunc=lambda : self.get_this_weeks_user_entries(userid),
                 expiretime=86400)

            for w, t in zip(users_this_week, users_today):
                w['count'] += t['count']

            my_alerts.append({'label': 'This Week', 'items': users_this_week})
            my_alerts.append({'label': 'Today', 'items': users_today})

            alerts.append({'label': label, 'alerts': my_alerts})

        all_alerts = []
        # cache for 5 minutes
        today = c.get_value(key='today',
                            createfunc=self.get_todays_entries,
                            expiretime=300)

        # cache for a day
        this_week = c.get_value(key='this_week',
                                createfunc=self.get_this_week_entries,
                                expiretime=86400)

        # add today's results to this_week as an optimization
        # e.g. this week only contains a count up to 11:59 of the
        #      previous day
        for w, t in zip(this_week, today):
            w['count'] += t['count']

        all_alerts.append({'label': 'This Week', 'items': this_week})
        all_alerts.append({'label': 'Today', 'items': today})
        alerts.append({'label': 'All Packages', 'alerts': all_alerts})

        d['alerts'] = alerts

    def query_builds_count(self, userid, before, after, state):
        # FIXME: Add this as an alerts query to the connector
        builds = get_connector('koji')

        id = None
        if userid:
            user = builds.call('getUser', params={'userInfo':userid})
            if user:
                id = user['id']

        if before:
            before = str(before)
        if after:
            after = str(after)

        params = dict(userID=id,
                      state=state,
                      completeBefore=before,
                      completeAfter=after,
                      queryOpts={'countOnly': True})

        # check if user exists
        if user_id and not user:
            count = 0
        else:
            count = builds.call('listBuilds', params)
            
        if state == 1:
            label = 'builds succeeded'
            icon = '16_success_build.png'
        elif state == 3:
            label = 'builds failed'
            icon = '16_failure_build.png'

        return {'count': count, 'label': label, 'state': state, 'icon': icon}

    def get_this_week_entries(self):
        bodhi = get_connector('bodhi')
        now = datetime.utcnow()
        a_day_ago = now - timedelta(days=1)
        a_day_ago = a_day_ago.replace(hour = 23,
                                      minute = 59,
                                      second = 59)
        week_start = now - timedelta(weeks=1)

        results = []

        complete_builds = self.query_builds_count(None, a_day_ago, week_start, 1)
        failed_builds = self.query_builds_count(None, a_day_ago, week_start, 3)
        stable_updates = bodhi.query_updates_count('stable',
                                                   before=a_day_ago,
                                                   after=week_start)
        testing_updates = bodhi.query_updates_count('testing',
                                                    before=a_day_ago,
                                                    after=week_start)

        complete_builds['url'] = '/package_maintenance/builds/successful'
        failed_builds['url'] = '/package_maintenance/builds/failed'
        stable_updates['url'] = '/package_maintenance/updates/stable_updates'
        testing_updates['url'] = '/package_maintenance/updates/testing_updates'
        stable_updates['icon'] = testing_updates['icon'] = '16_bodhi.png'

        results.append(complete_builds)
        results.append(failed_builds)
        results.append(stable_updates)
        results.append(testing_updates)

        return results

    def get_todays_entries(self):
        bodhi = get_connector('bodhi')
        today_start = datetime.utcnow()
        today_start = today_start.replace(hour = 0)
        results = []

        complete_builds = self.query_builds_count(None, None, today_start, 1)
        failed_builds = self.query_builds_count(None, None, today_start, 3)
        stable_updates = bodhi.query_updates_count('stable', after=today_start)
        testing_updates = bodhi.query_updates_count('testing',after=today_start)

        complete_builds['url'] = '/package_maintenance/builds/successful'
        failed_builds['url'] = '/package_maintenance/builds/failed'
        stable_updates['url'] = '/package_maintenance/updates/stable_updates'
        testing_updates['url'] = '/package_maintenance/updates/testing_updates'
        stable_updates['icon'] = testing_updates['icon'] = '16_bodhi.png'

        results.append(complete_builds)
        results.append(failed_builds)
        results.append(stable_updates)
        results.append(testing_updates)

        return results

    def get_todays_user_entries(self, userid):
        bodhi = get_connector('bodhi')
        now = datetime.utcnow()
        today_start = datetime.utcnow()
        today_start = today_start.replace(hour = 0)
        results = []

        complete_builds = self.query_builds_count(userid, None, today_start, 1)
        failed_builds = self.query_builds_count(userid, None, today_start, 3)
        stable_updates = bodhi.query_updates_count('stable',
                                                   username=userid,
                                                   after=today_start)
        testing_updates = bodhi.query_updates_count('testing',
                                                    username=userid,
                                                    after=today_start)

        complete_builds['url'] = '/my_profile/package_maintenance/builds_succeeded'
        failed_builds['url'] = '/my_profile/package_maintenance/builds_failed'
        stable_updates['url'] = '/my_profile/package_maintenance/stable_updates'
        testing_updates['url'] = '/my_profile/package_maintenance/testing_updates'
        stable_updates['icon'] = testing_updates['icon'] = '16_bodhi.png'

        results.append(complete_builds)
        results.append(failed_builds)
        results.append(stable_updates)
        results.append(testing_updates)

        return results

    def get_this_weeks_user_entries(self, userid):
        bodhi = get_connector('bodhi')
        now = datetime.utcnow()
        a_day_ago = now - timedelta(days=1)
        a_day_ago = a_day_ago.replace(hour = 23,
                                      minute = 59,
                                      second = 59)
        week_start = now - timedelta(weeks=1)

        results = []

        complete_builds = self.query_builds_count(userid, week_start, a_day_ago, 1)
        failed_builds = self.query_builds_count(userid, week_start, a_day_ago, 3)
        stable_updates = bodhi.query_updates_count('stable',
                                                   username=userid,
                                                   before=a_day_ago,
                                                   after=week_start)
        testing_updates = bodhi.query_updates_count('testing',
                                                    username=userid,
                                                    before=a_day_ago,
                                                    after=week_start)

        complete_builds['url'] = '/my_profile/package_maintenance/builds_succeeded'
        failed_builds['url'] = '/my_profile/package_maintenance/builds_failed'
        stable_updates['url'] = '/my_profile/package_maintenance/stable_updates'
        testing_updates['url'] = '/my_profile/package_maintenance/testing_updates'
        stable_updates['icon'] = testing_updates['icon'] = '16_bodhi.png'

        results.append(complete_builds)
        results.append(failed_builds)
        results.append(stable_updates)
        results.append(testing_updates)

        return results

alerts_container = AlertsContainer('alerts')

class RootController(Controller):

    @expose('mako:moksha.templates.widget')
    @validate({'profile': validators.StringBool()})
    def index(self, username=None, profile=False):
        tmpl_context.widget = alerts_container
        return dict(options={'userid': username, 'profile': profile})
