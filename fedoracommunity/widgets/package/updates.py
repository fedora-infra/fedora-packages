import tw2.core as twc

from fedoracommunity.widgets.grid import Grid
from fedoracommunity.connectors.api import get_connector

from fedoracommunity.widgets.expander import expander_js

bodhi_js = twc.JSLink(filename='static/javascript/bodhi.js',
                      modname=__name__)

class Updates(Grid):
    template = 'mako:fedoracommunity.widgets.package.templates.updates_table_widget'
    kwds = twc.Param()
    package_name = twc.Param('The name of the package to view')
    release_table = twc.Param()
    resource = 'bodhi'
    resource_path = 'query_updates'
    resources = Grid.resources + [bodhi_js, expander_js]

    def prepare(self):
        self.package_name = self.kwds['package_name']
        self.subpackage_of = self.kwds.get('subpackage_of', '')
        self.total_rows = -1
        main_pkg = self.package_name
        if self.subpackage_of:
            main_pkg = self.subpackage_of

        self.filters = {'package': main_pkg}
        self.rows_per_page = 10

        releases = []
        # This is the same collection table.  Same as the other two widgets.
        pkgdb = get_connector('pkgdb')
        collections = pkgdb.get_collection_table(active_only=True)

        for id, collection in collections.items():
            name = collection['name']
            ver = collection['version']
            label = "%s %s" % (name, ver)
            branchname = collection['branchname']
            value = ""
            if branchname:
                value = branchname
            if label != 'Fedora devel' and name in ('Fedora', 'Fedora EPEL'
):
                releases.append({
                    'label': label,
                    'value': value,
                    'version': ver,
                    })

        def _sort(a,b):
            return cmp(int(b['version']), int(a['version']))

        releases.sort(_sort)
        self.release_table = releases

        # Must do this last for our Grids
        super(Updates, self).prepare()
