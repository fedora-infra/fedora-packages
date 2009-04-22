from tg import expose, tmpl_context
from pylons import cache, request
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

        # cache for a minute
        users = []
        if d.get('profile') or d.get('userid'):
            label = 'Error if you see this label'
            if d.get('profile'):
                label = 'Your Recent Packages'
                creds = request.environ.get('repoze.what.credentials')
                if creds and creds.get('repoze.what.userid'):
                    userid = creds.get('repoze.what.userid')
            else:
                userid = d.get('userid')
                label = '%s\'s Recent Packages' % userid

            users_data = c.get_value(key=userid,
                 createfunc=lambda : self.get_user_entries(userid),
                 expiretime=3600)

            d['alerts'] = [{'label': label, 'items': users_data}]
        else:
            # cache for 5 minutes
            today = c.get_value(key='today',
                                createfunc=self.get_todays_entries,
                                expiretime=300)

            # cache for a day
            this_week = c.get_value(key='this_week',
                                    createfunc=self.get_this_week_entries,
                                    expiretime=3600)

            # add today's results to this_week as an optimization
            # e.g. this week only contains a count up to 11:59 of the
            #      previous day
            for w, t in zip(this_week, today):
                w['count'] += t['count']

            d['alerts'] = [{'label': 'This Week', 'items': this_week},
                           {'label': 'Today', 'items': today}]

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

        complete_builds['url'] = '/package_maintenance/builds/success'
        failed_builds['url'] = '/package_maintenance/builds/fail'
        stable_updates['url'] = '/package_maintenance/updates/stable'
        testing_updates['url'] = '/package_maintenance/updates/testing'
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
        stable_updates['url'] = '/package_maintenance/updates/stable'
        testing_updates['url'] = '/package_maintenance/updates/testing'
        stable_updates['icon'] = testing_updates['icon'] = '16_bodhi.png'

        results.append(complete_builds)
        results.append(failed_builds)
        results.append(stable_updates)
        results.append(testing_updates)

        return results

    def get_user_entries(self, userid):
        bodhi = get_connector('bodhi')
        now = datetime.utcnow()
        week_start = now - timedelta(weeks=1)
        results = []

        complete_builds = self.query_builds_count(userid, None, week_start, 1)
        failed_builds = self.query_builds_count(userid, None, week_start, 3)
        stable_updates = bodhi.query_updates_count('stable',
                                                   username=userid,
                                                   after=week_start)
        testing_updates = bodhi.query_updates_count('testing',
                                                    username=userid,
                                                    after=week_start)

        complete_builds['url'] = '/profile/builds/my_successful'
        failed_builds['url'] = '/profile/builds/my_failed'
        stable_updates['url'] = '/profile/updates/stable'
        testing_updates['url'] = '/profile/updates/testing'
        stable_updates['icon'] = testing_updates['icon'] = '16_bodhi.png'

        results.append(complete_builds)
        results.append(failed_builds)
        results.append(stable_updates)
        results.append(testing_updates)

        return results

alerts_container = AlertsContainer('alerts')

class RootController(Controller):

    @expose('mako:moksha.templates.widget')
    def index(self, username=None):
        tmpl_context.widget = alerts_container
        return dict(options={'userid': username})
