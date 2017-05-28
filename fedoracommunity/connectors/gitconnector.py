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

import re
import os
import git
import logging
import subprocess

from tg import config
from kitchen.text.converters import to_unicode
from moksha.common.lib.dates import DateTimeDisplay

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
        if out:
            log.debug(out)
        if err:
            log.error(err)
        return out

    def clone_repo(self):
        """ Create a fresh clone of this package's git repository """
        self._run('fedpkg clone --anonymous --branches ' + self.package,
                  cwd=config.get('git_repo_path'))

    def get_spec(self):
        """ Return the contents of this package's RPM spec file """
        if os.path.exists(os.path.join(self.repo_path, 'dead.package')):
            return to_unicode(
                self.repo.tree()['dead.package'].data_stream.read())
        return to_unicode(
            self.repo.tree()[self.package + '.spec'].data_stream.read())

    def get_patches(self):
        """ Return a dictionary of all patches for this package """
        patches = []
        for patch in [blob for blob in self.repo.tree().traverse()
                      if blob.name.endswith('.patch')]:
            created = self.get_creation_time(patch.name)
            patches.append({
                'name': patch.name,
                'date': created.strftime('%d %b %Y'),
                'datetime': created,
                'age': DateTimeDisplay(created).age(granularity='day',
                                                    general=True),
                })
        return sorted(
            patches, cmp=lambda x, y: cmp(x['datetime'], y['datetime']))

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
                        current['msg'] += to_unicode('%s\n' % ' '.join(chunks))
        commits.append(current)
        self.inject_links(commits)
        return commits

    def inject_links(self, commits):
        """
        Iterate over all of the commits and link up bug numbers and CVEs.
        """
        bug_url = ('<a href="https://bugzilla.redhat.com/show_bug.cgi?id=%s'
                   '" target="_blank">%s</a>')
        cve_url = ('<a href="http://cve.mitre.org/cgi-bin/cvename.cgi?name=%s"'
                   ' target="_blank">%s</a>')
        regexs = (r'#(\d+)', r'[rR][hH][bB][zZ]:? ?(\d+)',
                  r'[bB][zZ]:? ?(\d+)', r'[Bb]ug:? ?(\d+)')
        for commit in commits:
            for regex in regexs:
                for bug in re.findall(regex, commit['msg']):
                    commit['msg'] = commit['msg'].replace(
                        bug, bug_url % (bug, bug))
            # Link up CVE IDs
            for cve in re.findall(r'(CVE-\d\d\d\d-\d\d\d\d)', commit['msg']):
                commit['msg'] = commit['msg'].replace(
                    cve, cve_url % (cve, cve))

    def get_diffstat(self, patch='*.patch'):
        """ Return the output of diffstat on a given patch, or all patches """
        return self._run('diffstat %s' % patch)

    def get_creation_time(self, filename):
        """ Return a datetime object for the date a given file was created """
        data = self.repo.git.log(filename, reverse=True)
        lines = (l for l in data.split('\n') if l.startswith('Date'))
        date = ' '.join(lines.next().split()[1:-1])
        fmt = '%a %b %d %H:%M:%S %Y'
        return DateTimeDisplay(date, format=fmt).datetime

    def get_source_url(self):
        source = self._run('spectool -S *.spec')
        if source:
            return source.split()[1]

    def get_fedora_source(self):
        url = config.get(
            'fedora_lookaside', 'https://src.fedoraproject.org/repo/pkgs')
        source = self.get_source_url()
        if source:
            tarball = source.split('/')[-1]
            md5 = self._run('grep %s sources' % tarball).split()[0]
            url += '/%s/%s/%s/%s' % (self.package, tarball, md5, tarball)
            return url
