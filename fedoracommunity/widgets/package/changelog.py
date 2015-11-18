import tw2.core as twc
from fedoracommunity.widgets.grid import Grid

class ChangelogGrid(Grid):
    template='mako:fedoracommunity.widgets.package.templates.changelog_table_widget'
    resource='koji'
    resource_path='query_changelogs'

    def prepare(self):

        # TODO - get these from from the 'active releases' connector.
        self.all_releases = [
            'rawhide',
        ]

        self.filters = {
            'package_name': self.package_name,
            'release': self.all_releases[0],
        }
        self.rows_per_page = 10

        # Must do this last for our Grids
        super(ChangelogGrid, self).prepare()


class ChangelogWidget(twc.Widget):
    template = 'mako:fedoracommunity.widgets.package.templates.changelog'
    changelog_grid = ChangelogGrid
