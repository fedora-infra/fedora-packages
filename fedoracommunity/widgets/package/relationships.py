import tw2.core as twc
import collections

from package import TabWidget
from mako.template import Template
from moksha.api.connectors import get_connector
from moksha.api.widgets import Grid

class RelationshipsNavWidget(TabWidget):
    tabs = collections.OrderedDict([('Requires', 'package.relationships.requires'),
                                    ('Depends', 'package.relationships.depends'),
                                    ('Provides', 'package.relationships.provides'),
                                    ('Obsoletes', 'package.relationships.obsoletes'),
                                    ('Conflicts', 'package.relationships.conflicts')])
    base_url = Template(text='/${kwds["package_name"]}/relationships/')
    default_tab = 'Requires'


class RelationshipsWidget(twc.Widget):
    template = 'mako:fedoracommunity.widgets.package.templates.relationships'
    args = twc.Param()
    kwds = twc.Param()
    nav_widget = RelationshipsNavWidget

class RelationshipBaseWidget(twc.Widget):
    template = 'mako:fedoracommunity.widgets.package.templates.relationshipbase'

    def prepare(self):
        super(RelationshipBaseWidget, self).prepare()

        self.package_name = self.kwds['package_name']
        xapian = get_connector('xapian')
        koji = get_connector('koji')
        latest_builds = xapian.get_latest_builds(self.package_name)
        self.default_build_id = latest_builds['Rawhide']['build_id']
        self.latest_builds = latest_builds
        build_ids = []
        for build_info in self.latest_builds.values():
            build_ids.append(build_info['build_id'])

        self.default_build_id = build_ids[0]

        tasks = koji.get_tasks_for_builds(build_ids)

        self.build_to_archtask_map = {}
        # filter tasks to only contain buildArch tasks
        for build_info in self.latest_builds.values():
            arch_tasks = []

            for subtasks in tasks[build_info['build_id']].values():
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

class RequiresWidget(RelationshipBaseWidget):
    pass

class DependsWidget(RelationshipBaseWidget):
    pass

class ProvidesWidget(RelationshipBaseWidget):
    pass

class ObsoletesWidget(RelationshipBaseWidget):
    pass

class ConflictsWidget(RelationshipBaseWidget):
    pass




