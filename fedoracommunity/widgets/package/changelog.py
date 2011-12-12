import tw2.core as twc
from moksha.api.widgets.grid import TW2Grid
from moksha.api.connectors import get_connector

class ChangelogGrid(TW2Grid):
    template='mako:fedoracommunity.widgets.package.templates.changelog_table_widget'
    resource='koji'
    resource_path='query_changelogs'

    def prepare(self):
        self.filters = {'build_id': self.build_id}
        self.rows_per_page = 10

        # Must do this last for our Grids
        super(ChangelogGrid, self).prepare()


class ChangelogWidget(twc.Widget):
    template = 'mako:fedoracommunity.widgets.package.templates.changelog'
    changelog_grid = ChangelogGrid

    def prepare(self):
        self.package_name = self.kwds['package_name']
        xapian = get_connector('xapian')
        latest_builds = xapian.get_latest_builds(self.package_name)
        self.default_build_id = latest_builds['Rawhide']['build_id']
        self.latest_builds = latest_builds

