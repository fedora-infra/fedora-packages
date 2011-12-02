import os
import git
import subprocess
import tw2.core as twc
import logging

from tg import config
from mako.template import Template
from collections import OrderedDict
from moksha.lib.helpers import DateTimeDisplay
from pygments import highlight
from pygments.lexers import DiffLexer
from pygments.formatters import HtmlFormatter

from package import TabWidget

log = logging.getLogger(__name__)

class FedoraGitRepo(object):

    def __init__(self, package, branch='master'):
        self.package = package
        self.branch = branch
        top_repo = config.get('git_repo_path')
        self.repo_path = os.path.join(top_repo, package, branch)
        if not os.path.isdir(self.repo_path):
            if not os.path.isdir(top_repo):
                os.makedirs(top_repo)
            self.clone_repo()
        self.repo = git.Repo(self.repo_path)

    def _run(self, cmd, **kw):
        # if no working directory is specified, default to inside the
        # repo for this package & branch
        if 'cwd' not in kw:
            kw['cwd'] = self.repo_path
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, **kw)
        out, err = p.communicate()
        if out: log.debug(out)
        if err: log.error(err)
        return out

    def clone_repo(self):
        self._run('fedpkg clone --anonymous --branches ' + self.package,
                  cwd=config.get('git_repo_path'))

    def get_spec(self):
        return self.repo.tree()[self.package + '.spec'].data_stream.read()

    def get_patches(self):
        patches = {}
        for patch in [blob for blob in self.repo.tree().traverse()
                      if blob.name.endswith('.patch')]:
            created = self.get_creation_time(patch.name)
            patches[patch.name] = [
                DateTimeDisplay(created).age(granularity='day', general=True),
                created.strftime('%d %b %Y'),
                ]
        return patches

    def get_patch(self, filename):
        return self.repo.tree()[filename].data_stream.read()

    def get_patch_changelog(self, patch):
        commits = []
        current = {}
        in_commit = False
        for commit in self.repo.git.log(patch).split('\n'):
            chunks = commit.split()
            if chunks:
                if chunks[0] == 'commit':
                    if current:
                        commits.append(current)
                    current = {'msg': ''}
                elif chunks[0] == 'Author:':
                    current['author'] = ' '.join(chunks[1:])
                elif chunks[0] == 'Date:':
                    current['date'] = DateTimeDisplay(
                        ' '.join(chunks[1:-1]),
                        format='%a %b %d %H:%M:%S %Y').datetime
                else:
                        current['msg'] += '%s\n' % ' '.join(chunks)
        commits.append(current)
        return commits

    def get_diffstat(self, patch='*.patch'):
        return self._run('diffstat %s' % patch)

    def get_creation_time(self, filename):
        date = ' '.join(self.repo.git.log(filename, reverse=True).split('\n')[2].split()[1:-1])
        return DateTimeDisplay(date, format='%a %b %d %H:%M:%S %Y').datetime

class Sources(TabWidget):
    tabs = OrderedDict([
        ('Spec', 'package.sources.spec'),
        ('Patches', 'package.sources.patches'),
        ('Diffs', 'package.sources.diffs'),
        ('Tarballs', 'package.sources.tarballs'),
        ('Git', 'package.sources.git'),
        ])
    base_url = Template(text='/${kwds["package_name"]}/sources/')
    default_tab = 'Spec'


class Spec(twc.Widget):
    kwds = twc.Param(default=None)
    text = twc.Param('The text of the specfile')
    template = 'mako:fedoracommunity/widgets/package/templates/package_spec.mak'

    def prepare(self):
        super(Spec, self).prepare()
        repo = FedoraGitRepo(self.kwds['package_name'])
        self.text = repo.get_spec()


class Patches(twc.Widget):
    kwds = twc.Param(default=None)
    patches = twc.Param(default=None)
    package = twc.Variable()
    diffstat = twc.Variable()
    template = 'mako:fedoracommunity/widgets/package/templates/patches.mak'

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
    template = 'mako:fedoracommunity/widgets/package/templates/patch.mak'

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
    template = 'mako:fedoracommunity/widgets/package/templates/diffs.mak'
    def prepare(self):
        super(Diffs, self).prepare()


class Tarballs(twc.Widget):
    template = 'mako:fedoracommunity/widgets/package/templates/tarballs.mak'
    kwds = twc.Param(default=None)

    def prepare(self):
        super(Tarballs, self).prepare()


class GitRepo(twc.Widget):
    template = 'mako:fedoracommunity/widgets/package/templates/git.mak'
    kwds = twc.Param(default=None)

    def prepare(self):
        super(GitRepo, self).prepare()
