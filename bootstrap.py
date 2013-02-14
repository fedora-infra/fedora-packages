# -*- coding: utf-8 -*-
# This file is part of Fedora Packages.
# Copyright (C) 2012  Red Hat, Inc.
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
import sys
import subprocess


def run(cmd):
    print(cmd)
    subprocess.call(cmd, shell=True)


def install_deps():
    """ Should only be run once. First-time moksha setup. """
    if os.path.exists('/etc/redhat-release'):
        reqs = [
            'python-kitchen', 'python-fedora', 'python-bugzilla', 'koji',
            'xapian-bindings-python', 'diffstat', 'fedpkg', 'svn', 'wget',
            'python-xappy', 'python-webob', 'moksha', 'TurboGears2',
            'python-dogpile-cache', 'python-dogpile-core',
            'python-retask', 'python-memcached',
        ]
        run('sudo yum install -q -y --enablerepo=updates-testing ' + ' '.join(reqs))


snapshot_url = 'http://lmacken.fedorapeople.org/fedora-packages'


def download_db_snapshot():
    """ Download a snapshot of our xapian database """
    run('wget -N %s/xapian-LATEST.tar.xz' % snapshot_url)
    run('tar xvf xapian-LATEST.tar.xz')


def download_icons():
    """ Download a snapshot of all package icons """
    icon_dir = 'fedoracommunity/public/images/'
    if not os.path.isdir(icon_dir + 'icons'):
        run('wget -N %s/icons.tar.xz' % snapshot_url)
        run('tar xvf icons.tar.xz')
        run('mv icons %s' % icon_dir)


def link_external_libs():
    """ Link rpm modules in from the system site-packages. """
    location = 'python{major}.{minor}/site-packages'.format(
        major=sys.version_info.major, minor=sys.version_info.minor)
    template = 'ln -s /usr/{location}/{lib} {venv}/{location}/'
    for lib in ['koji', 'rpm', 'rpmUtils', 'fedora', 'kitchen', 'pycurl',
                'yum', 'urlgrabber', 'sqlitecachec', '_sqlitecache',
                'bugzilla', 'xapian', 'xappy',
                'dogpile', 'memcache'
               ]:
        for libdir in ('lib64', 'lib'):
            for ext in ('.py', '.so', ''):
                mod = '/usr/%s/%s/%s%s' % (libdir, location, lib, ext)
                if os.path.exists(mod):
                    template = 'ln -s /usr/{libdir}/{location}/{lib}{ext} {venv}/{libdir}/{location}/'
                    cmd = template.format(libdir=libdir, ext=ext, lib=lib,
                                          venv=os.environ['VIRTUAL_ENV'],
                                          location=location)
                    print cmd
                    run(cmd)


def develop():
    run('%s setup.py develop' % sys.executable)


if __name__ == '__main__':
    install_deps()
    link_external_libs()
    develop()
    download_db_snapshot()
    download_icons()
