import tw2.core as twc
from moksha.api.widgets import Grid
from moksha.api.connectors import get_connector
from collections import OrderedDict

class FilelistTree(twc.Widget):
    template='mako:fedoracommunity.widgets.package.templates.filelist_tree_widget'

    def prepare(self):
        super(FilelistTree, self).prepare()


class ContentsWidget(twc.Widget):
    template = 'mako:fedoracommunity.widgets.package.templates.contents'
    # filelist_tree = FilelistTree

    def prepare(self):
        super(ContentsWidget, self).prepare()

        self.package_name = self.kwds['package_name']
        xapian = get_connector('xapian')
        koji = get_connector('koji')
        latest_builds = xapian.get_latest_builds(self.package_name)
        self.default_build_id = latest_builds['Rawhide']['build_id']
        self.latest_builds = latest_builds
        build_ids = []
        for build_info in self.latest_builds.values():
            build_id = build_info['build_id']
            if build_id:
                build_ids.append(build_id)

        self.default_build_id = build_ids[0]

        tasks = koji.get_tasks_for_builds(build_ids)

        self.build_to_archtask_map = {}
        # filter tasks to only contain buildArch tasks
        for build_info in self.latest_builds.values():
            arch_tasks = []

            build_tasks = tasks.get(build_info['build_id'], None)
            if not build_tasks:
                continue

            for subtasks in build_tasks.values():
                for task in subtasks:
                    if task['method'] == 'buildArch':
                        arch_tasks.append(task)
                        name = self.package_name
                        version = build_info['version']
                        release = build_info['release']
                        arch = task['label']
                        nvr = "%s-%s-%s" % (name, version, release)
                        filename = "%s.%s.rpm" % (nvr, arch)
                        task['nvr'] = nvr
                        task['filename'] = filename

            build_info['arch_tasks'] = arch_tasks
            self.build_to_archtask_map[build_info['build_id']] = arch_tasks

