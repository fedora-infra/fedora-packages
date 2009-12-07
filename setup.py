#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of Fedora Community.
# Copyright (C) 2008-2009  Red Hat, Inc.
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
    ('fedoracommunity/public/images', filter(os.path.isfile, glob.glob('fedoracommunity/public/images/*'))),
    ('fedoracommunity/public/images/banners', filter(os.path.isfile, glob.glob('fedoracommunity/public/images/banners/*'))),
    ('fedoracommunity/public/images/planet-bubbles', filter(os.path.isfile, glob.glob('fedoracommunity/public/images/planet-bubbles/*'))),
    ('fedoracommunity/public/images/tour', filter(os.path.isfile, glob.glob('fedoracommunity/public/images/tour/*'))),
    ('fedoracommunity/public/images/tour/screenshots', filter(os.path.isfile, glob.glob('fedoracommunity/public/images/tour/screenshots/*'))),
    ('fedoracommunity/public/misc', filter(os.path.isfile, glob.glob('fedoracommunity/public/misc/*'))),
    ('fedoracommunity/public/javascript', filter(os.path.isfile, glob.glob('fedoracommunity/public/javascript/*.js'))),
]

packages = find_packages(exclude=['ez_setup'])

setup(
    name='fedoracommunity',
    version='0.3.8.2',
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
        "pytz",
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
    fedoracommunity_appchrome_css = fedoracommunity.widgets:fedoracommunity_appchrome_css
    fedoracommunity_branding_css = fedoracommunity.widgets:fedoracommunity_branding_css
    jquery_template_js = fedoracommunity.widgets:jquery_template_js
    jquery_json_js = fedoracommunity.widgets:jquery_json_js
    jquery_ui_tabs = tw.jquery.ui_tabs:jquery_ui_tabs_js

    [moksha.connector]
    koji = fedoracommunity.connectors:KojiConnector
    bodhi = fedoracommunity.connectors:BodhiConnector
    pkgdb = fedoracommunity.connectors:PkgdbConnector
    fas = fedoracommunity.connectors:FasConnector
    bugzilla = fedoracommunity.connectors:BugzillaConnector
    planet = fedoracommunity.connectors:PlanetConnector
    yum = fedoracommunity.connectors:YumConnector
    wiki = fedoracommunity.connectors:WikiConnector

    [moksha.application]
    login = fedoracommunity.mokshaapps.login:RootController
    fedoracommunity.mokshatest = fedoracommunity.mokshaapps.mokshatest:RootController
    fedoracommunity = fedoracommunity.mokshaapps.fedoracommunity:RootController

    fedoracommunity.overviewresource = fedoracommunity.mokshaapps.overviewresource:RootController
    fedoracommunity.myprofileresource = fedoracommunity.mokshaapps.myprofileresource:RootController
    fedoracommunity.packagemaintresource = fedoracommunity.mokshaapps.packagemaintresource:RootController
    fedoracommunity.peopleresource = fedoracommunity.mokshaapps.peopleresource:RootController

    fedoracommunity.search = fedoracommunity.mokshaapps.searchresource:RootController

    fedoracommunity.builds = fedoracommunity.mokshaapps.builds:RootController
    fedoracommunity.updates = fedoracommunity.mokshaapps.updates:RootController
    fedoracommunity.alerts = fedoracommunity.mokshaapps.alerts:RootController
    fedoracommunity.packages = fedoracommunity.mokshaapps.packages:RootController
    fedoracommunity.people = fedoracommunity.mokshaapps.people:RootController
    fedoracommunity.statistics = fedoracommunity.mokshaapps.statistics:RootController
    fedoracommunity.demos = fedoracommunity.mokshaapps.demos:RootController

    [moksha.widget]
    fedoracommunity.login = fedoracommunity.widgets.login:LoginWidget
    fedoracommunity.planet = fedoracommunity.widgets.planet:PlanetFedoraWidget
    fedoracommunity.quicklinks = fedoracommunity.widgets.quicklinks:QuickLinksWidget
    fedoracommunity.bodhi = fedoracommunity.widgets.bodhi:bodhi_js
    fedoracommunity.demos.amqp = fedoracommunity.mokshaapps.demos.controllers.root:kamaloka_qpid_js
    placeholder = moksha.api.widgets:Placeholder
    grid = moksha.api.widgets:Grid
    clock = fedoracommunity.widgets.clock:clock_js
    expander = fedoracommunity.widgets.expander:expander_js
    

    [moksha.stream]
    stats_cla_done = fedoracommunity.streams.stats:ClaDoneDataStream
    wiki_all_revisions = fedoracommunity.streams.stats:WikiAllRevisionsDataStream

    [moksha.extension_point]
    fedoracommunity = fedoracommunity.plugins.extensions

    """
)
