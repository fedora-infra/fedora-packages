import tw2.core as twc
from moksha.api.widgets import Grid

class ActiveReleasesGrid(Grid):
    template = 'mako:fedoracommunity.widgets.package.templates.active_releases'
    package_name = twc.Param('The name of the package to view')
    resource = 'bodhi'
    resource_path = 'query_active_releases'

    def prepare(self):
        self.filters = {'package': self.package_name}
        self.rows_per_page = 10

        # Must do this last for our Grids
        super(ActiveReleasesGrid, self).prepare()
