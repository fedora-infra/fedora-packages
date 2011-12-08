import tw2.core as twc
from moksha.api.widgets.grid import TW2Grid

class BuildsGrid(TW2Grid):
    template='mako:fedoracommunity.widgets.package.templates.builds_table_widget'
    resource='koji'
    resource_path='query_builds'

    def prepare(self):
        self.filters = {'package': self.package_name}
        self.rows_per_page = 10

        # Must do this last for our Grids
        super(BuildsGrid, self).prepare()


class Builds(twc.Widget):
    template = 'mako:fedoracommunity.widgets.package.templates.builds'
    in_progress_builds = BuildsGrid
