import tw2.core as twc
from fedoracommunity.widgets.grid import Grid

class ProblemsGrid(Grid):
    template='mako:fedoracommunity.widgets.package.templates.problems_table_widget'
    resource='faf'
    resource_path='query_problems'

    def prepare(self):
        self.filters = {
            'package_name' : self.package_name
        }

        self.rows_per_page = 10

        # Must do this last for our Grids
        super(ProblemsGrid, self).prepare()


class ProblemsWidget(twc.Widget):
    template = 'mako:fedoracommunity.widgets.package.templates.problems'
    problems_grid = ProblemsGrid
