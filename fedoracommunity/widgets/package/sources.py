# This file is part of Fedora Community.
# Copyright (C) 2011  Red Hat, Inc.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import tw2.core as twc

from tg import config
from mako.template import Template
from fedoracommunity.lib.utils import OrderedDict
from pygments import highlight
from pygments.lexers import DiffLexer
from pygments.formatters import HtmlFormatter
from fedoracommunity.connectors.api import get_connector

from fedoracommunity.connectors.gitconnector import FedoraGitRepo
from fedoracommunity.lib.utils import RpmSpecLexer
from package import TabWidget

class Sources(TabWidget):
    tabs = OrderedDict([
        ('Patches', 'package_sources_patches'),
        ('Spec', 'package_sources_spec'),
        #('Diffs', 'package.sources.diffs'),
        #('Tarballs', 'package.sources.tarballs'),
        #('Git', 'package.sources.git'),
        ])
    base_url = Template(text='/${kwds["package_name"]}/sources/')
    default_tab = 'Patches'

class ReleaseFilter(twc.Widget):
    on_change = twc.Param('The name of the javascript function to call upon change')
    package = twc.Param('The name of the package')
    template = 'mako:fedoracommunity.widgets.package.templates.release_filter'

    def prepare(self):
        super(ReleaseFilter, self).prepare()
        releases = []
        top_repo = os.path.join(config.get('git_repo_path'), self.package)
        # XXX - This is the collection table, just like in the bugs widget.
        pkgdb = get_connector('pkgdb')
        collections = pkgdb.get_collection_table(active_only=True)
        for id, collection in collections.iteritems():
            name = collection['name']
            ver = collection['version']
            label = "%s %s" % (name, ver)
            value = ""
            branchname = collection['branchname']
            if branchname:
                repo_path = os.path.join(top_repo, branchname)
                if not os.path.isdir(repo_path):
                    continue
                value = branchname
            if label != 'Fedora devel' and name in ('Fedora', 'Fedora EPEL'):
                releases.append({
                    'label': label,
                    'value': value,
                    'version': ver,
                    })
        self.releases_table = sorted(releases, reverse=True,
                cmp=lambda x, y: cmp(x['version'], y['version']))
        self.releases_table.insert(0, {'label': 'Rawhide', 'value': 'master'})


class Spec(twc.Widget):
    kwds = twc.Param(default=None)
    text = twc.Variable('The text of the specfile')
    template = 'mako:fedoracommunity.widgets.package.templates.package_spec'
    releases = ReleaseFilter

    def prepare(self):
        super(Spec, self).prepare()
        self.package_name = self.kwds['package_name']
        self.subpackage_of = self.kwds.get('subpackage_of')
        self.branch = self.kwds.get('branch', 'master')
        if self.subpackage_of:
            main_package = self.subpackage_of
        else:
            main_package = self.package_name
        repo = FedoraGitRepo(main_package, branch=self.branch)
        self.text = highlight(repo.get_spec(), RpmSpecLexer(),
                HtmlFormatter(full=True, linenos=True, nobackground=True))


class Patches(twc.Widget):
    kwds = twc.Param(default=None)
    patches = twc.Param(default={})
    package = twc.Variable()
    diffstat = twc.Variable(default='')
    releases = ReleaseFilter
    template = 'mako:fedoracommunity.widgets.package.templates.patches'

    def prepare(self):
        super(Patches, self).prepare()
        self.package = self.kwds['package_name']
        self.subpackage_of = self.kwds.get('subpackage_of')
        if self.subpackage_of:
            main_package = self.subpackage_of
        else:
            main_package = self.package
        self.branch = self.kwds.get('branch', 'master')
        repo = FedoraGitRepo(main_package, branch=self.branch)
        self.patches = repo.get_patches()
        self.diffstat = repo.get_diffstat()


class Patch(twc.Widget):
    kwds = twc.Param()
    diffstat = twc.Param('The diffstat for this patch', default=True)
    text = twc.Variable('The text of the patch')
    changelog = twc.Variable('The changelog of this patch')
    template = 'mako:fedoracommunity.widgets.package.templates.patch'

    def prepare(self):
        super(Patch, self).prepare()
        self.package = self.kwds['package']
        self.subpackage_of = self.kwds.get('subpackage_of')
        self.patch = self.kwds['patch']
        self.branch = self.kwds['branch']
        if self.subpackage_of:
            main_package = self.subpackage_of
        else:
            main_package = self.package
        repo = FedoraGitRepo(main_package, branch=self.branch)
        diff = repo.get_patch(self.patch)
        if self.diffstat:
            self.diffstat = repo.get_diffstat(self.patch)
        self.text = highlight(diff, DiffLexer(),
                HtmlFormatter(full=True, nobackground=True))
        self.changelog = repo.get_patch_changelog(self.patch)


class Diffs(twc.Widget):
    template = 'mako:fedoracommunity.widgets.package.templates.diffs'
    def prepare(self):
        super(Diffs, self).prepare()


class Tarballs(twc.Widget):
    template = 'mako:fedoracommunity.widgets.package.templates.tarballs'
    package = twc.Param('The name of the package')
    upstream_tarball = twc.Variable(default=None)
    kwds = twc.Param(default=None)
    releases = ReleaseFilter

    def prepare(self):
        super(Tarballs, self).prepare()
        self.package = self.kwds['package_name']
        self.subpackage_of = self.kwds.get('subpackage_of')
        self.branch = self.kwds.get('branch', 'master')
        if self.subpackage_of:
            main_package = self.subpackage_of
        else:
            main_package = self.package
        repo = FedoraGitRepo(main_package, branch=self.branch)
        self.upstream_tarball = repo.get_source_url()
        self.fedora_tarball = repo.get_fedora_source()


class GitRepo(twc.Widget):
    template = 'mako:fedoracommunity.widgets.package.templates.git'
    kwds = twc.Param(default=None)

    def prepare(self):
        super(GitRepo, self).prepare()
