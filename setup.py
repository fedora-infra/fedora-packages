#!/usr/bin/env python
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
   ('fedoracommunity/public/misc', filter(os.path.isfile, glob.glob('fedoracommunity/public/misc/*'))),
   ('fedoracommunity/public/javascript', filter(os.path.isfile, glob.glob('fedoracommunity/public/javascript/*.js'))),
]

packages = find_packages(exclude=['ez_setup'])

setup(
    name='fedoracommunity',
    version='0.2',
    description='',
    author='John (J5) Palmieri',
    author_email='johnp@redhat.com',
    #url='',
    install_requires=[
        "moksha",
        "Pylons",
        "PyOpenSSL",
        ],
    packages=packages,
    include_package_data=True,
    test_suite='nose.collector',
    tests_require=['webtest'],
    namespace_packages=['fedoracommunity'],
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
    myfedora_appchrome_css = fedoracommunity.widgets:myfedora_appchrome_css
    myfedora_branding_css = fedoracommunity.widgets:myfedora_branding_css
    myfedora_js = fedoracommunity.widgets:myfedora_js
    myfedora_extension_js = fedoracommunity.widgets:myfedora_extensions_js
    myfedora_ui_js = fedoracommunity.widgets:myfedora_ui_js
    jquery_template_js = fedoracommunity.widgets:jquery_template_js
    jquery_json_js = fedoracommunity.widgets:jquery_json_js
    jquery_ui_tabs = tw.jquery.ui_tabs:jquery_ui_tabs_js

    [moksha.connector]
    koji = fedoracommunity.connectors:KojiConnector
    bodhi = fedoracommunity.connectors:BodhiConnector
    pkgdb = fedoracommunity.connectors:PkgdbConnector
    fas = fedoracommunity.connectors:FasConnector

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

    [moksha.widget]
    fedoracommunity.login = fedoracommunity.widgets.login:LoginWidget
    fedoracommunity.planet = fedoracommunity.widgets.planet:PlanetFedoraWidget
    grid = moksha.api.widgets:Grid
    placeholder = moksha.api.widgets:Placeholder


    [moksha.extension_point]
    fedoracommunity = fedoracommunity.plugins.extensions
    """
)
