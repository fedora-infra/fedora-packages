import tw2.core as twc

from moksha.api.widgets.grid import TW2Grid
from moksha.api.connectors import get_connector

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


class BugsGrid(TW2Grid):
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
