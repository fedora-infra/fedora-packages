#!/usr/bin/env python

try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

setup(
    name='myfedora',
    version='0.1',
    description='',
    author='',
    author_email='',
    #url='',
    install_requires=[
        "TurboGears2",
        ],
    packages=find_packages(exclude=['ez_setup']),
    include_package_data=True,
    test_suite='nose.collector',
    package_data={'myfedora': ['i18n/*/LC_MESSAGES/*.mo',
                                 'templates/*/*',
                                 'public/*/*']},
    #message_extractors = {'myfedora': [
    #        ('**.py', 'python', None),
    #        ('templates/**.mako', 'mako', None),
    #        ('templates/**.html', 'genshi', None),
    #        ('public/**', 'ignore', None)]},

    entry_points="""
    [paste.app_factory]
    main = myfedora.config.middleware:make_app

    [paste.app_install]
    main = pylons.util:PylonsInstaller

    [myfedora.plugins.resourceviews]
    packages = myfedora.plugins.resourceviews.packages:PackagesViewApp
    people = myfedora.plugins.resourceviews.people:PeopleViewApp

    [myfedora.plugins.resourceviews.packages.tools]
    info = myfedora.plugins.tools.packageinfo:PackageInfoToolWidget
    builds = myfedora.plugins.tools.builds:BuildsToolWidget

    [myfedora.plugins.resourceviews.people.tools]
    builds = myfedora.plugins.tools.builds:BuildsToolWidget

    [myfedora.data]
    rss = myfedora.apps.rss:FedoraPeopleData

    [myfedora.apps]
    rss = myfedora.apps.rss:FedoraPeopleApp
    helloworld = myfedora.apps.helloworld:HelloWorldApp
    sandbox = myfedora.apps.sandbox:SandboxApp
    navigation = myfedora.apps.navigation:NavigationApp

    [myfedora.apps.rss.views]
    home = myfedora.apps.rss:FedoraPeopleWidget
    canvas = myfedora.apps.rss:FedoraPeopleWidget 
    profile = myfedora.apps.rss:FedoraPeopleWidget 
    preview = myfedora.apps.rss:FedoraPeopleWidget
    config = myfedora.apps.rss:FedoraPeopleWidget
    
    [myfedora.apps.helloworld.views]
    home = myfedora.apps.helloworld:HelloWorldWidget
    canvas = myfedora.apps.helloworld:HelloWorldWidget
    profile = myfedora.apps.helloworld:HelloWorldWidget
    preview = myfedora.apps.helloworld:HelloWorldWidget
    config = myfedora.apps.helloworld:HelloWorldWidget
    
    [myfedora.apps.sandbox.views]
    home = myfedora.apps.sandbox:SandboxHomeWidget
    canvas = myfedora.apps.sandbox:SandboxHomeWidget
    profile = myfedora.apps.sandbox:SandboxHomeWidget 
    preview = myfedora.apps.sandbox:SandboxHomeWidget
    config = myfedora.apps.sandbox:SandboxHomeWidget


    [myfedora.apps.navigation.views]
    home = myfedora.apps.navigation:NavigationWidget
    canvas = myfedora.apps.navigation:NavigationWidget 
    profile = myfedora.apps.navigation:NavigationWidget
    preview = myfedora.apps.navigation:NavigationWidget
    config = myfedora.apps.navigation:NavigationWidget
    """,
)
