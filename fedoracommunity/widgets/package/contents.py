import tw2.core as twc

from fedoracommunity.widgets.tree import tree_js

class FilelistTree(twc.Widget):
    template='mako:fedoracommunity.widgets.package.templates.filelist_tree_widget'

    def prepare(self):
        super(FilelistTree, self).prepare()


class ContentsWidget(twc.Widget):
    resources = [tree_js]
    template = 'mako:fedoracommunity.widgets.package.templates.contents'
    # filelist_tree = FilelistTree

    def prepare(self):
        super(ContentsWidget, self).prepare()

        self.package_name = self.kwds['package_name']
        self.subpackage_of = self.kwds.get('subpackage_of', '')

        # TODO - get these from from the 'active releases' connector.
        self.repos = ['rawhide']
