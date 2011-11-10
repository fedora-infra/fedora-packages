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

import os
import glob

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
    version='0.4.1',
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
        "xappy",
        #"pytz",
        ],
    scripts=['fedoracommunity_makeyumcache'],
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

    [moksha.global]
    fedora_css = fedoracommunity.widgets:fedora_css
    fedoracommunity_reset_css = fedoracommunity.widgets:fedoracommunity_reset_css
    fedoracommunity_text_css = fedoracommunity.widgets:fedoracommunity_text_css
    fedoracommunity_960_24_col_cs = fedoracommunity.widgets:fedoracommunity_960_24_col_css
    fedoracommunity_appchrome_css = fedoracommunity.widgets:fedoracommunity_appchrome_css
    fedoracommunity_branding_css = fedoracommunity.widgets:fedoracommunity_branding_css
    jquery_json_js = moksha.widgets.json:jquery_json_js
    #jquery_ui_tabs = tw.jquery.ui_tabs:jquery_ui_tabs_js
    moksha_js = moksha.widgets.moksha_js:moksha_js
    jquery_template_js = moksha.widgets.jquery_template:jquery_template_js

    [moksha.connector]
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
    fedoracommunity.bodhi = fedoracommunity.widgets.bodhi:bodhi_js
    grid = moksha.api.widgets:Grid

    package.overview = fedoracommunity.widgets.package:OverviewWidget
    package.overview.details = fedoracommunity.widgets.package.overview:Details
    package.overview.updates = fedoracommunity.widgets.package.updates:Updates
    package.overview.builds = fedoracommunity.widgets.package.builds:Builds

    package.bugs = fedoracommunity.widgets.package.bugs:BugsWidget


    [moksha.stream]
    stats_cla_done = fedoracommunity.streams.stats:ClaDoneDataStream
    wiki_all_revisions = fedoracommunity.streams.stats:WikiAllRevisionsDataStream

    [moksha.extension_point]
    fedoracommunity = fedoracommunity.plugins.extensions

    """
)
