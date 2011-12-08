import tw2.core as twc
import collections

from package import TabWidget
from mako.template import Template
from moksha.api.connectors import get_connector
from moksha.api.widgets.grid import TW2Grid

class RelationshipsNavWidget(TabWidget):
    tabs = collections.OrderedDict([('Requires', 'package.relationships.requires'),
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

class RequiresGridWidget(TW2Grid):
    template = 'mako:fedoracommunity.widgets.package.templates.requires_table_widget'
    resource = 'koji'
    resource_path = 'query_requires'
    onReady = "update_grid()"

class ProvidesGridWidget(TW2Grid):
    template = 'mako:fedoracommunity.widgets.package.templates.provides_table_widget'
    resource = 'koji'
    resource_path = 'query_provides'
    onReady = "update_grid()"

class ObsoletesGridWidget(TW2Grid):
    template = 'mako:fedoracommunity.widgets.package.templates.obsoletes_table_widget'
    resource = 'koji'
    resource_path = 'query_obsoletes'
    onReady = "update_grid()"

class ConflictsGridWidget(TW2Grid):
    template = 'mako:fedoracommunity.widgets.package.templates.conflicts_table_widget'
    resource = 'koji'
    resource_path = 'query_conflicts'
    onReady = "update_grid()"

class RequiresWidget(RelationshipBaseWidget):
    grid = RequiresGridWidget

class DependsWidget(RelationshipBaseWidget):
    pass

class ProvidesWidget(RelationshipBaseWidget):
    grid = ProvidesGridWidget

class ObsoletesWidget(RelationshipBaseWidget):
    grid = ObsoletesGridWidget

class ConflictsWidget(RelationshipBaseWidget):
    grid = ConflictsGridWidget




