import tw2.core as twc
import datetime

from fedoracommunity.widgets.grid import Grid
from fedoracommunity.connectors.api import get_connector


class BugStatsWidget(twc.Widget):
    template = "mako:fedoracommunity.widgets.package.templates.bugs_stats_widget"
    id = twc.Param(default='bugs_widget')
    kwds = twc.Param(default=None)
    product = twc.Param(default='Fedora')
    version = twc.Param(default='rawhide')
    package = twc.Param(default=None)
    num_closed = twc.Param(default='-')
    num_open = twc.Param(default='-')
    num_new = twc.Param(default='-')
    num_new_this_week = twc.Param(default='')
    num_closed_this_week = twc.Param(default='')

    bz_prefix = "https://bugzilla.redhat.com/buglist.cgi"
    status_open_string = "bug_status=NEW&bug_status=ASSIGNED&bug_status=REOPENED"
    status_closed_string = "bug_status=CLOSED"

    base_query_string = twc.Variable(default='')
    open_query_string = twc.Variable(default='')
    closed_query_string = twc.Variable(default='')

    def prepare(self):
        super(BugStatsWidget, self).prepare()
        def to_query_string(query):
            return "&".join([
                "{key}={value}".format(key=key, value=value)
                for key, value in query.items()
            ])
        self.base_query_string = to_query_string({
            "query_format": "advanced",
            "product": self.product,
            "component": self.package,
        })
        self.open_query_string = to_query_string({
            "chfieldto": "Now",
            "chfield": "[Bug creation]",
            "chfieldfrom": datetime.datetime.now().isoformat().split('T')[0],
        })
        self.closed_query_string = to_query_string({
            "chfieldto": "Now",
            "chfield": "bug_status",
            "chfieldvalue": "CLOSED",
            "chfieldfrom": datetime.datetime.now().isoformat().split('T')[0],
        })


class BugsGrid(Grid):
    resource = 'bugzilla'
    resource_path = 'query_bugs'
    release_table = twc.Param()
    package = twc.Param()
    template = "mako:fedoracommunity.widgets.package.templates.bugs_table_widget"

    def prepare(self):
        releases = []
        self.filters = {'package': self.package}
        pkgdb = get_connector('pkgdb')
        collections = pkgdb.get_collection_table(active_only=True)

        for id, collection in collections.items():
            name = collection['name']
            ver = collection['version']
            label = "%s %s" % (name, ver)
            value = str(ver)
            if ver == 'devel':
                name = 'Rawhide'
                ver = 9999999
                label = 'Rawhide'
                value = 'rawhide'

            if name in ('Fedora', 'Rawhide', 'Fedora EPEL'):
                releases.append({'label': label, 'value': value, 'version': ver})

        def _sort(a,b):
            return cmp(int(b['version']), int(a['version']))

        releases.sort(_sort)
        self.release_table = releases

        super(BugsGrid, self).prepare()


class BugsWidget(twc.Widget):
    bug_stats = BugStatsWidget
    bug_grid = BugsGrid
    kwds = twc.Param()
    package = twc.Param()
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
