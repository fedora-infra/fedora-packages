#!/usr/bin/env python
# -*- coding: utf-8 -*-
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

import __main__; __main__.__requires__ = __requires__ = ['WebOb>=1.0']; import pkg_resources

import os
import glob

# These two imports are not actually used, but are required to stop tests from
# failing on python 2.7.
import multiprocessing
import logging

try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

data_files = [
    ('fedoracommunity/public', filter(os.path.isfile, glob.glob('fedoracommunity/public/*'))),
    ('fedoracommunity/public/css', filter(os.path.isfile, glob.glob('fedoracommunity/public/css/*.css'))),
    ('fedoracommunity/public/css/fonts', filter(os.path.isfile, glob.glob('fedoracommunity/public/css/fonts/*.ttf'))),
    ('fedoracommunity/public/css/filetreetheme', filter(os.path.isfile, glob.glob('fedoracommunity/public/css/filetreetheme/*'))),
    ('fedoracommunity/public/images', filter(os.path.isfile, glob.glob('fedoracommunity/public/images/*'))),
    ('fedoracommunity/public/images/banners', filter(os.path.isfile, glob.glob('fedoracommunity/public/images/banners/*'))),
    ('fedoracommunity/public/images/planet-bubbles', filter(os.path.isfile, glob.glob('fedoracommunity/public/images/planet-bubbles/*'))),
    ('fedoracommunity/public/images/icons', filter(os.path.isfile, glob.glob('fedoracommunity/public/images/icons/*'))),
    ('fedoracommunity/public/images/tour', filter(os.path.isfile, glob.glob('fedoracommunity/public/images/tour/*'))),
    ('fedoracommunity/public/images/tour/screenshots', filter(os.path.isfile, glob.glob('fedoracommunity/public/images/tour/screenshots/*'))),
    ('fedoracommunity/public/misc', filter(os.path.isfile, glob.glob('fedoracommunity/public/misc/*'))),
    ('fedoracommunity/public/javascript', filter(os.path.isfile, glob.glob('fedoracommunity/public/javascript/*.js'))),
]

packages = find_packages(exclude=['ez_setup'])

setup(
    name='fedoracommunity',
    version='0.5.0',
    description='',
    license='AGPLv3',
    authors=('John (J5) Palmieri <johnp@redhat.com>',
             'Luke Macken <lmacken@redhat.com>',
             'Máirín Duffy <duffy@redhat.com>',
             ),
    url='http://fedoracommunity.fedorahosted.org',
    install_requires=[
        "moksha",
        #"PyOpenSSL",
        "SQLAlchemy>=0.5",
        #"xappy",
        # For some reason this doesn't get automatically pulled in :(
        #"GitPython",
        #"pytz",
        ],
    scripts=['fedoracommunity_makeyumcache', 'bin/fcomm-index-packages', 'bin/fcomm-index-latest-builds'],
    packages=packages,
    include_package_data=True,
    test_suite='nose.collector',
    tests_require=['webtest'],
    data_files=data_files,
    package_data={'fedoracommunity': ['i18n/*/LC_MESSAGES/*.mo']
                               },
    #message_extractors = {'myfedora': [
    #        ('**.py', 'python', None),
    #        ('templates/**.mako', 'mako', None),
    #        ('templates/**.html', 'genshi', None),
    #        ('public/**', 'ignore', None)]},

    entry_points="""
    [setuptools.file_finders]
    git = fedoracommunity.lib.utils:find_git_files

    [paste.app_factory]
    main = fedoracommunity.config.middleware:make_app

    [paste.app_install]
    main = pylons.util:PylonsInstaller

#    [fas.repoze.who.metadata_plugins]
#    blog_info = myfedora.plugins.identity.bloginfo:add_metadata

    # list all the widgets we need for deployment - this is messy but the
    # easiest way to get things working
    [tw2.widgets]
    widgets = fedoracommunity.widgets
    moksha_js = moksha.widgets.moksha_js
    fcomm_js = fedoracommunity.connectors.widgets:fcomm_js
    moksha_widgets = moksha.api.widgets
    bodhi_js = fedoracommunity.widgets.package.updates:bodhi_js

    fedoracommunity.bodhi_js = fedoracommunity.widgets.package.updates:bodhi_js
    fedoracommunity.updates = fedoracommunity.widgets.package.updates:Updates

    packages = fedoracommunity.widgets.package

    package.overview = fedoracommunity.widgets.package.overview
    package.updates = fedoracommunity.widgets.package.updates
    package.builds = fedoracommunity.widgets.package.builds

    package.bugs = fedoracommunity.widgets.package.bugs
    package.contents = fedoracommunity.widgets.package.contents
    package.changelog = fedoracommunity.widgets.package.changelog
    package.sources = fedoracommunity.widgets.package.sources

    package.relationships = fedoracommunity.widgets.package.relationships

    [moksha.global]
    fedora_css = fedoracommunity.widgets:fedora_css
    fedoracommunity_reset_css = fedoracommunity.widgets:fedoracommunity_reset_css
    fedoracommunity_text_css = fedoracommunity.widgets:fedoracommunity_text_css
    fedoracommunity_960_24_col_cs = fedoracommunity.widgets:fedoracommunity_960_24_col_css
    fedoracommunity_appchrome_css = fedoracommunity.widgets:fedoracommunity_appchrome_css
    fedoracommunity_branding_css = fedoracommunity.widgets:fedoracommunity_branding_css
    #jquery_json_js = moksha.widgets.json:jquery_json_js
    #jquery_ui_tabs = tw.jquery.ui_tabs:jquery_ui_tabs_js
    #moksha_js = moksha.widgets.moksha_js:moksha_js
    #jquery_template_js = moksha.widgets.jquery_template:jquery_template_js

    [fcomm.connector]
    koji = fedoracommunity.connectors:KojiConnector
    bodhi = fedoracommunity.connectors:BodhiConnector
    pkgdb = fedoracommunity.connectors:PkgdbConnector
    fas = fedoracommunity.connectors:FasConnector
    bugzilla = fedoracommunity.connectors:BugzillaConnector
    planet = fedoracommunity.connectors:PlanetConnector
    yum = fedoracommunity.connectors:YumConnector
    xapian = fedoracommunity.connectors:XapianConnector
    wiki = fedoracommunity.connectors:WikiConnector
    torrent = fedoracommunity.connectors:TorrentConnector

    [moksha.widget]
    fedoracommunity.bodhi = fedoracommunity.widgets.package.updates:Updates
    grid = fedoracommunity.widgets.grid:Grid

    package.overview = fedoracommunity.widgets.package.overview:Details

    package.updates = fedoracommunity.widgets.package.updates:Updates
    package.builds = fedoracommunity.widgets.package.builds:Builds
    package.bugs = fedoracommunity.widgets.package.bugs:BugsWidget
    package.contents = fedoracommunity.widgets.package.contents:ContentsWidget
    package.changelog = fedoracommunity.widgets.package.changelog:ChangelogWidget
    package.sources = fedoracommunity.widgets.package.sources:Sources
    package.sources.spec = fedoracommunity.widgets.package.sources:Spec
    package.sources.patches = fedoracommunity.widgets.package.sources:Patches
    package.sources.patch = fedoracommunity.widgets.package.sources:Patch
    package.sources.diffs = fedoracommunity.widgets.package.sources:Diffs
    package.sources.tarballs = fedoracommunity.widgets.package.sources:Tarballs
    package.sources.git = fedoracommunity.widgets.package.sources:GitRepo

    package.relationships = fedoracommunity.widgets.package.relationships:RelationshipsWidget
    package.relationships.requires = fedoracommunity.widgets.package.relationships:RequiresWidget
    package.relationships.requiredby = fedoracommunity.widgets.package.relationships:RequiredByWidget
    package.relationships.depends = fedoracommunity.widgets.package.relationships:DependsWidget
    package.relationships.provides = fedoracommunity.widgets.package.relationships:ProvidesWidget
    package.relationships.obsoletes = fedoracommunity.widgets.package.relationships:ObsoletesWidget
    package.relationships.conflicts = fedoracommunity.widgets.package.relationships:ConflictsWidget

    [moksha.stream]
    stats_cla_done = fedoracommunity.streams.stats:ClaDoneDataStream
    wiki_all_revisions = fedoracommunity.streams.stats:WikiAllRevisionsDataStream

    [moksha.extension_point]
    fedoracommunity = fedoracommunity.plugins.extensions

    [distutils.commands]
    archive_fedoracommunity_resources = fedoracommunity.distutils.command:archive_fedoracommunity_resources

    """
)
