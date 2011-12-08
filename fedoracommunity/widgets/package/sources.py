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

import tw2.core as twc

from mako.template import Template
from collections import OrderedDict
from pygments import highlight
from pygments.lexers import DiffLexer, BashLexer
from pygments.formatters import HtmlFormatter
from moksha.api.connectors import get_connector

from fedoracommunity.connectors.gitconnector import FedoraGitRepo
from package import TabWidget

class Sources(TabWidget):
    tabs = OrderedDict([
        ('Spec', 'package.sources.spec'),
        ('Patches', 'package.sources.patches'),
        #('Diffs', 'package.sources.diffs'),
        ('Tarballs', 'package.sources.tarballs'),
        #('Git', 'package.sources.git'),
        ])
    base_url = Template(text='/${kwds["package_name"]}/sources/')
    default_tab = 'Spec'


class ReleaseFilter(twc.Widget):
    on_change = twc.Param('The name of the javascript function to call upon change')
    template = 'mako:fedoracommunity.widgets.package.templates.release_filter'

    def prepare(self):
        super(ReleaseFilter, self).prepare()
        releases = []
        pkgdb = get_connector('pkgdb')
        collections = pkgdb.get_collection_table(active_only=True)
        for id, collection in collections.iteritems():
            name = collection['name']
            ver = collection['version']
            label = "%s %s" % (name, ver)
            value = ""
            branchname = collection['gitbranchname']
            if branchname:
                value = branchname
            if label != 'Fedora devel' and name in ('Fedora', 'Fedora EPEL'):
                releases.append({
                    'label': label,
                    'value': value,
                    'version': ver,
                    })
        self.releases_table = sorted(releases,
                cmp=lambda x, y: cmp(x['version'], y['version']))
        self.releases_table.insert(0, {'label': 'Rawhide', 'value': 'master'})


class Spec(twc.Widget):
    kwds = twc.Param(default=None)
    text = twc.Param('The text of the specfile')
    template = 'mako:fedoracommunity.widgets.package.templates.package_spec'
    releases = ReleaseFilter

    def prepare(self):
        super(Spec, self).prepare()
        self.package_name = self.kwds['package_name']
        repo = FedoraGitRepo(self.package_name)
        self.text = highlight(repo.get_spec(), BashLexer(),
                HtmlFormatter(full=True, linenos=True, nobackground=True))


class Patches(twc.Widget):
    kwds = twc.Param(default=None)
    patches = twc.Param(default=None)
    package = twc.Variable()
    diffstat = twc.Variable()
    template = 'mako:fedoracommunity.widgets.package.templates.patches'

    def prepare(self):
        super(Patches, self).prepare()
        self.package = self.kwds['package_name']
        repo = FedoraGitRepo(self.package)
        self.patches = repo.get_patches()
        self.diffstat = repo.get_diffstat()


class Patch(twc.Widget):
    package = twc.Param('The name of the package')
    patch = twc.Param('The filename of the patch')
    diffstat = twc.Param('The diffstat for this patch', default=True)
    text = twc.Variable('The text of the patch')
    changelog = twc.Variable('The changelog of this patch')
    template = 'mako:fedoracommunity.widgets.package.templates.patch'

    def prepare(self):
        super(Patch, self).prepare()
        repo = FedoraGitRepo(self.package)
        diff = repo.get_patch(self.patch)
        if self.diffstat:
            self.diffstat = repo.get_diffstat(self.patch)
        self.text = highlight(diff, DiffLexer(),
                HtmlFormatter(full=True, linenos=True, nobackground=True))
        self.changelog = repo.get_patch_changelog(self.patch)


class Diffs(twc.Widget):
    template = 'mako:fedoracommunity.widgets.package.templates.diffs'
    def prepare(self):
        super(Diffs, self).prepare()


class Tarballs(twc.Widget):
    template = 'mako:fedoracommunity.widgets.package.templates.tarballs'
    package = twc.Param('The name of the package')
    upstream_tarball = twc.Variable()
    kwds = twc.Param(default=None)

    def prepare(self):
        super(Tarballs, self).prepare()
        self.package = self.kwds['package_name']
        repo = FedoraGitRepo(self.package)
        self.upstream_tarball = repo.get_source_url()
        self.fedora_tarball = repo.get_fedora_source()


class GitRepo(twc.Widget):
    template = 'mako:fedoracommunity.widgets.package.templates.git'
    kwds = twc.Param(default=None)

    def prepare(self):
        super(GitRepo, self).prepare()
