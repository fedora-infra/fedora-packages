import tw2.core as twc
from fedoracommunity.widgets.grid import Grid

class ProblemsGrid(Grid):
    template='mako:fedoracommunity.widgets.package.templates.problems_table_widget'
    resource='faf'
    resource_path='query_problems'

    def prepare(self):
        self.package = self.package_name

        # Must do this last for our Grids
        super(ProblemsGrid, self).prepare()


class Problems(twc.Widget):
    template = 'mako:fedoracommunity.widgets.package.templates.problems'
    in_progress_builds = ProblemsGrid

    def prepare(self):
        super(Problems, self).prepare()
        subpackage_of = self.kwds.get('subpackage_of', '')

        if subpackage_of:
            self.main_package = subpackage_of
        else:
            self.main_package = self.kwds['package_name']
