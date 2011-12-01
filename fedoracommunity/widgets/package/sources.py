import os
import git
import subprocess
import tw2.core as twc
import logging

from tg import config
from mako.template import Template
from collections import OrderedDict
from moksha.lib.helpers import DateTimeDisplay

from package import TabWidget

log = logging.getLogger(__name__)

class FedoraGitRepo(object):

    def __init__(self, package, branch='master'):
        self.package = package
        top_repo = config.get('git_repo_path')
        self.repo_path = os.path.join(top_repo, package, branch)
        if not os.path.isdir(self.repo_path):
            if not os.path.isdir(top_repo):
                os.makedirs(top_repo)
            self.clone_repo()
        self.repo = git.Repo(self.repo_path)

    def _run(self, cmd, **kw):
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, **kw)
        out, err = p.communicate()
        if out: log.debug(out)
        if err: log.error(err)
        return p.returncode

    def clone_repo(self):
        self._run('fedpkg clone --anonymous --branches ' + self.package,
                  cwd=config.get('git_repo_path'))

    def get_spec(self):
        spec = self.repo.tree()[self.package + '.spec']
        return spec.data_stream.read()

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
    template = 'mako:fedoracommunity/widgets/package/templates/patches.mak'

    def prepare(self):
        super(Patches, self).prepare()
        repo = FedoraGitRepo(self.kwds['package_name'])
        self.patches = repo.get_patches()


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
