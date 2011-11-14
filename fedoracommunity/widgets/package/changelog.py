import tw2.core as twc
from moksha.api.widgets import Grid
from moksha.api.connectors import get_connector
from collections import OrderedDict

class ChangelogGrid(Grid):
    template='mako:fedoracommunity.widgets.package.templates.changelog_table_widget'
    resource='koji'
    resource_path='query_changelogs'

    def prepare(self):
        self.filters = {'build_id': self.build_id,
                        'task_id':  self.task_id,
                        'state': self.state}
        self.rows_per_page = 10

        # Must do this last for our Grids
        super(ChangelogGrid, self).prepare()


class ChangelogWidget(twc.Widget):
    template = 'mako:fedoracommunity.widgets.package.templates.changelog'
    changelog_grid = ChangelogGrid

    def prepare(self):
        self.package_name = self.kwds['package_name']
        koji = get_connector('koji')
        try:
            # FIXME for now hardcode this but we really should have some sort
            # of mapping of releases to tags
            tags = ({'name': 'Rawhide', 'tag': 'dist-rawhide'},
                    {'name': 'Fedora 16', 'tag': 'f16'},
                    {'name': 'Fedora 16', 'tag': 'f16-updates'},
                    {'name': 'Fedora 16 Testing', 'tag': 'f16-updates-testing'},
                    {'name': 'Fedora 15', 'tag': 'dist-f15'},
                    {'name': 'Fedora 15', 'tag': 'dist-f15-updates'},
                    {'name': 'Fedora 15 Testing', 'tag': 'dist-f15-updates-testing'},
                    {'name': 'Fedora 14', 'tag': 'dist-f14'},
                    {'name': 'Fedora 14', 'tag': 'dist-f14-updates'},
                    {'name': 'Fedora 14 Testing', 'tag': 'dist-f14-updates-testing'},
                    {'name': 'EPEL 6', 'tag': 'dist-6E-epel-base'},
                    {'name': 'EPEL 6', 'tag': 'dist-6E-epel'},
                    {'name': 'EPEL 6', 'tag': 'dist-6E-epel-testing'},
                    {'name': 'EPEL 5', 'tag': 'dist-5E-base'},
                    {'name': 'EPEL 5', 'tag': 'dist-5E-epel'},
                    {'name': 'EPEL 5', 'tag': 'dist-5E-epel-testing'},
                    )

            latest_builds = OrderedDict()
            for t in tags:
                tag = t['tag']
                builds = koji._koji_client.getLatestBuilds(tag, package=self.package_name)
                if builds:
                    build = builds[0]
                    latest_builds[t['name']] = {'nvr': build['nvr'],
                                                'build_id': build['build_id'],
                                                'task_id': build['task_id'],
                                                'state': build['state']}

            self.default_build_id = latest_builds['Rawhide']['build_id']
            self.default_task_id = latest_builds['Rawhide']['task_id']
            self.default_state = latest_builds['Rawhide']['state']
            self.latest_builds = latest_builds

        except Exception, e:
            print('Unable to query koji: %s' % str(e))
            self.latest_builds = 'Koji unavailable'
