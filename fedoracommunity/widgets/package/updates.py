import tw2.core as twc

from moksha.api.widgets import Grid
from moksha.api.connectors import get_connector

bodhi_js = twc.JSLink(filename='static/javascript/bodhi.js',
                      modname=__name__)

class Updates(Grid):
    template = 'mako:fedoracommunity.widgets.package.templates.updates_table_widget'
    kwds = twc.Param()
    package_name = twc.Param('The name of the package to view')
    release_table = twc.Param()
    resource = 'bodhi'
    resource_path = 'query_updates'

    def prepare(self):
        self.resources.append(bodhi_js)
        self.package_name = self.kwds['package_name']
        self.filters = {'package': self.package_name}
        self.rows_per_page = 10

        releases = []
        pkgdb = get_connector('pkgdb')
        collections = pkgdb.get_collection_table(active_only=True)

        for id, collection in collections.items():
            name = collection['name']
            ver = collection['version']
            label = "%s %s" % (name, ver)
            branchname = collection['gitbranchname']
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
