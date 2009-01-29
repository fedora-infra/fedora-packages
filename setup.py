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
        "Pylons"
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

    [fas.repoze.who.metadata_plugins]
    blog_info = myfedora.plugins.identity.bloginfo:add_metadata
    
    [moksha.connector]
    koji = fedoracommunity.connectors:KojiConnector
    bodhi = fedoracommunity.connectors:BodhiConnector
    
    [moksha.application]
    login = fedoracommunity.mokshaapps.login:RootController
    fedoracommunity.mokshatest = fedoracommunity.mokshaapps.mokshatest:RootController
    fedoracommunity = fedoracommunity.mokshaapps.fedoracommunity:RootController
    fedoracommunity.overviewresource = fedoracommunity.mokshaapps.overviewresource:RootController
    fedoracommunity.packagemaintresource = fedoracommunity.mokshaapps.packagemaintresource:RootController
    fedoracommunity.builds = fedoracommunity.mokshaapps.builds:RootController
    fedoracommunity.updates = fedoracommunity.mokshaapps.updates:RootController
    """
)
