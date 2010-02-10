# This file is part of Fedora Community.
# Copyright (C) 2008-2010  Red Hat, Inc.
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



import sys

from paver.easy import *
import paver.misctasks
import paver.virtual

HEADER = """This file is part of Fedora Community.
Copyright (C) 2008-2010  Red Hat, Inc.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>."""

options(
    version=Bunch(
        number="0.1",
        name="FedoraCommunity",
        api="1"
    ),
    build_top=path("build"),
    build_dir=lambda: options.build_top / "FedoraCommunity",
    license=Bunch(
        extensions = set([
            ("py", "#"), ("js", "//")
        ]),
        exclude=set([
            './ez_setup',
            './data',
            './tg2env',
            './docs',
        ])
    ),
    virtualenv=Bunch(
        packages_to_install=['pip'],
        paver_command_line="required"
    ),
    server=Bunch(
        address="",
        port=8080,
        try_build=False,
        dburl=None,
        async=False,
        config_file=path("development.ini")
    ),
)

@task
@needs(["minilib", "generate_setup", "setuptools.command.sdist"])
def sdist():
    pass

@task
@needs(["minilib", "generate_setup", "setuptools.command.bdist_egg"])
def bdist_egg():
    pass

def _apply_header_if_necessary(f, header, first_line, last_line):
    data = f.bytes()
    if data.startswith(header):
        debug("File is already tagged")
        return
    debug("Tagging %s", f)
    if data.startswith(first_line):
        pos = data.find(last_line) + len(last_line)
        data = data[pos:]
    data = header + data
    f.write_bytes(data)

@task
def license():
    """Tags the appropriate files with the license text."""
    cwd = path(".")
    info("Tagging license text")
    for extension, comment_marker in options.extensions:
        hlines = [comment_marker + " " + line for line in HEADER.split("\n")]
        header = "\n".join(hlines) + "\n\n"
        first_line = hlines[0]
        last_line = hlines[-1]
        for f in cwd.walkfiles("*.%s" % extension):
            exclude = False
            for pattern in options.exclude:
                if f.startswith(pattern):
                    exclude=True
                    break
            if exclude:
                continue
            _apply_header_if_necessary(f, header, first_line, last_line)

@task
def test():
    from os import system
    sh("nosetests")
    system("nosetests")
