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
from kitchen.text.converters import to_unicode

from package import TabWidget

log = logging.getLogger(__name__)

class FedoraGitRepo(object):
    """ An abstraction for working with packages in the Fedora Git repos """

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
        """ Run a shell command and return stdout.

        If no `cwd` is specified, default to inside the repo for this
        package & branch.
        """
        if 'cwd' not in kw:
            kw['cwd'] = self.repo_path
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, **kw)
        out, err = p.communicate()
        if out: log.debug(out)
        if err: log.error(err)
        return out

    def clone_repo(self):
        """ Create a fresh clone of this package's git repository """
        self._run('fedpkg clone --anonymous --branches ' + self.package,
                  cwd=config.get('git_repo_path'))

    def get_spec(self):
        """ Return the contents of this package's RPM spec file """
        return to_unicode(self.repo.tree()[self.package + '.spec'].data_stream.read())

    def get_patches(self):
        """ Return a dictionary of all patches for this package """
        patches = {}
        for patch in [blob for blob in self.repo.tree().traverse()
                      if blob.name.endswith('.patch')]:
            created = self.get_creation_time(patch.name)
            patches[patch.name] = [
                DateTimeDisplay(created).age(granularity='day', general=True),
                created.strftime('%d %b %Y'),
                ]
        return patches

    def get_patch(self, patch):
        """ Return the contents of a specific patch """
        return to_unicode(self.repo.tree()[patch].data_stream.read())

    def get_patch_changelog(self, patch):
        """ Return a list of the changes made to this patch """
        commits = []
        current = {}
        for commit in self.repo.git.log(patch).split('\n'):
            chunks = commit.split()
            if chunks:
                if chunks[0] == 'commit':
                    if current:
                        commits.append(current)
                    current = {'msg': ''}
                elif chunks[0] == 'Author:':
                    current['author'] = to_unicode(' '.join(chunks[1:]))
                elif chunks[0] == 'Date:':
                    current['date'] = DateTimeDisplay(
                        ' '.join(chunks[1:-1]),
                        format='%a %b %d %H:%M:%S %Y').datetime
                else:
                        current['msg'] += to_unicode('%s\n' %' '.join(chunks))
        commits.append(current)
        return commits

    def get_diffstat(self, patch='*.patch'):
        """ Return the output of diffstat on a given patch, or all patches """
        return self._run('diffstat %s' % patch)

    def get_creation_time(self, filename):
        """ Return a datetime object for the date a given file was created """
        date = ' '.join(self.repo.git.log(filename, reverse=True).split('\n')[2].split()[1:-1])
        return DateTimeDisplay(date, format='%a %b %d %H:%M:%S %Y').datetime

    def get_source_url(self):
        return self._run('spectool -S *.spec').split()[1]

    def get_fedora_source(self):
        url = config.get('fedora_lookaside', 'http://pkgs.fedoraproject.org/repo/pkgs')
        tarball = self.get_source_url().split('/')[-1]
        md5 = self._run('grep %s sources' % tarball).split()[0]
        url += '/%s/%s/%s/%s' % (self.package, tarball, md5, tarball)
        return url


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
    template = 'mako:fedoracommunity/widgets/package/templates/git.mak'
    kwds = twc.Param(default=None)

    def prepare(self):
        super(GitRepo, self).prepare()
