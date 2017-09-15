import tw2.core as twc
import datetime
import urllib

from fedoracommunity.widgets.grid import Grid
from fedoracommunity.connectors.api import get_connector


class BugStatsWidget(twc.Widget):
    template = "mako:fedoracommunity.widgets.package.templates.bugs_stats_widget"
    id = twc.Param(default='bugs_widget')
    kwds = twc.Param(default=None)
    product = twc.Param(default='Fedora')
    version = twc.Param(default='rawhide')
    epel_version = twc.Param(default='el6')
    num_open = twc.Param(default='-')

    bz_prefix = "https://bugzilla.redhat.com/buglist.cgi"
    status_open_string = "bug_status=NEW&bug_status=ASSIGNED&bug_status=REOPENED"
    status_closed_string = "bug_status=CLOSED"

    base_query_string = twc.Variable(default='')

    def prepare(self):
        super(BugStatsWidget, self).prepare()
        self.base_query_string = urllib.urlencode({
            "query_format": "advanced",
            "product": self.product,
            "component": self.package,
        })


class BugsGrid(Grid):
    resource = 'bugzilla'
    resource_path = 'query_bugs'
    release_table = twc.Param()
    template = "mako:fedoracommunity.widgets.package.templates.bugs_table_widget"

    def prepare(self):

        # Signify that we haven't loaded any bugs yet.
        self.total_rows = -1

        releases = []
        self.filters = {'package': self.package}
        bodhi = get_connector('bodhi')

        for collection in bodhi.get_all_releases():
            if collection['state'] != 'current':
                continue
            name = collection['id_prefix']
            ver = collection['version']
            label = collection['long_name']
            value = str(ver)

            if name in ('FEDORA', 'Rawhide', 'FEDORA-EPEL'):
                releases.append({'label': label, 'value': value, 'version': ver})

        releases.append({'label': 'Rawhide', 'value': 'rawhide', 'version': 9999999})

        def _sort(a,b):
            return cmp(int(b['version']), int(a['version']))

        releases.sort(_sort)
        self.release_table = releases

        super(BugsGrid, self).prepare()


class BugsWidget(twc.Widget):
    bug_stats = BugStatsWidget
    bug_grid = BugsGrid
    kwds = twc.Param()
    template = "mako:fedoracommunity.widgets.package.templates.bugs"

    def prepare(self):
        super(BugsWidget, self).prepare()
        self.package = self.kwds['package_name']
        self.main_package = self.kwds.get('subpackage_of', '')

        if not self.main_package:
            self.main_package = self.package

        # This is here so you can hit packages/kernel/bugs/all
        if self.args == ['all']:
            self.children[1].rows_per_page = 100000
