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
    tests_require=['webtest'],
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

    [fas.repoze.who.metadata_plugins]
    blog_info = myfedora.plugins.identity.bloginfo:add_metadata

    [myfedora.plugins.resourceviews]
    profile = myfedora.plugins.resourceviews.profile:ProfileViewApp
    packages = myfedora.plugins.resourceviews.packages:PackagesViewApp
    people = myfedora.plugins.resourceviews.people:PeopleViewApp
    search = myfedora.plugins.resourceviews.search:SearchViewApp

    [myfedora.plugins.resourceviews.packages.tools]
    info = myfedora.plugins.apps.tools.packageinfo:PackageInfoToolWidget
    builds = myfedora.plugins.apps.tools.builds:BuildsToolWidget
    updates = myfedora.plugins.apps.tools.updates:UpdatesToolWidget

    [myfedora.plugins.resourceviews.people.tools]
    info = myfedora.plugins.apps.tools.userinfo:UserInfoToolWidget
    builds = myfedora.plugins.apps.tools.builds:BuildsToolWidget
    fedoramemberships = myfedora.plugins.apps.tools.fedoramemberships:FedoraMembershipsToolWidget
    updates = myfedora.plugins.apps.tools.updates:UpdatesToolWidget
    
    [myfedora.plugins.resourceviews.profile.tools]
    info = myfedora.plugins.apps.tools.profileinfo:ProfileInfoToolWidget
    builds = myfedora.plugins.apps.tools.builds:BuildsToolWidget
    fedoramemberships = myfedora.plugins.apps.tools.fedoramemberships:FedoraMembershipsToolWidget
    updates = myfedora.plugins.apps.tools.updates:UpdatesToolWidget
    
    [myfedora.plugins.resourceviews.search.tools]
    packages = myfedora.plugins.apps.tools.searchpackages:SearchPackagesToolWidget
    people = myfedora.plugins.apps.tools.searchpeople:SearchPeopleToolWidget
    
    [myfedora.data]
    rss = myfedora.plugins.apps.rss:FedoraPeopleData

    [myfedora.plugins.apps]
    planetfedora = myfedora.plugins.apps.planetfedora:PlanetFedoraApp
    helloworld = myfedora.plugins.apps.helloworld:HelloWorldApp
    sandbox = myfedora.plugins.apps.sandbox:SandboxApp
    navigation = myfedora.plugins.apps.navigation:NavigationApp
    login = myfedora.plugins.apps.login:LoginApp
    placeholder = myfedora.plugins.apps.placeholder:PlaceholderApp
    packagesnav = myfedora.plugins.apps.packagesnav:PackagesNavApp
    buildstable = myfedora.plugins.apps.buildstable:BuildsTableApp
    fedoraannounce = myfedora.plugins.apps.fedoraannounce:FedoraAnnounceApp
    peoplealphalist = myfedora.plugins.apps.peoplealphalist:PeopleAlphaListApp
    useralerts = myfedora.plugins.apps.useralerts:UserAlertsApp
    updates = myfedora.plugins.apps.updates:FedoraUpdatesApp
    
    #TOOLS:
    tools.packageinfo = myfedora.plugins.apps.tools.packageinfo:PackageInfoToolApp
    tools.builds = myfedora.plugins.apps.tools.builds:BuildsToolApp
    tools.helloworld = myfedora.plugins.apps.tools.helloworld:HelloWorldToolApp
    tools.searchall = myfedora.plugins.apps.tools.searchall:SearchAllToolApp
    tools.searchpackages = myfedora.plugins.apps.tools.searchpackages:SearchPackagesToolApp
    tools.searchpeople = myfedora.plugins.apps.tools.searchpeople:SearchPeopleToolApp
    tools.fedoramemberships = myfedora.plugins.apps.tools.fedoramemberships:FedoraMembershipsToolApp

    [myfedora.plugins.apps.planetfedora.views]
    home = myfedora.plugins.apps.planetfedora:PlanetFedoraHomeWidget
    canvas = myfedora.plugins.apps.planetfedora:PlanetFedoraCanvasWidget
    profile = myfedora.plugins.apps.planetfedora:PlanetFedoraHomeWidget
    preview = myfedora.plugins.apps.planetfedora:PlanetFedoraHomeWidget
    config = myfedora.plugins.apps.planetfedora:PlanetFedoraHomeWidget
    
    [myfedora.plugins.apps.helloworld.views]
    home = myfedora.plugins.apps.helloworld:HelloWorldWidget
    canvas = myfedora.plugins.apps.helloworld:HelloWorldWidget
    profile = myfedora.plugins.apps.helloworld:HelloWorldWidget
    preview = myfedora.plugins.apps.helloworld:HelloWorldWidget
    config = myfedora.plugins.apps.helloworld:HelloWorldWidget
    
    [myfedora.plugins.apps.sandbox.views]
    home = myfedora.plugins.apps.sandbox:SandboxHomeWidget
    canvas = myfedora.plugins.apps.sandbox:SandboxHomeWidget
    profile = myfedora.plugins.apps.sandbox:SandboxHomeWidget 
    preview = myfedora.plugins.apps.sandbox:SandboxHomeWidget
    config = myfedora.plugins.apps.sandbox:SandboxHomeWidget

    [myfedora.plugins.apps.navigation.views]
    home = myfedora.plugins.apps.navigation:NavigationWidget
    canvas = myfedora.plugins.apps.navigation:NavigationWidget 
    profile = myfedora.plugins.apps.navigation:NavigationWidget
    preview = myfedora.plugins.apps.navigation:NavigationWidget
    config = myfedora.plugins.apps.navigation:NavigationWidget
    
    [myfedora.plugins.apps.login.views]
    home = myfedora.plugins.apps.login:LoginWidget
    canvas = myfedora.plugins.apps.login:LoginWidget 
    
    [myfedora.plugins.apps.placeholder.views]
    home = myfedora.plugins.apps.placeholder:PlaceholderHomeWidget
    canvas = myfedora.plugins.apps.placeholder:PlaceholderCanvasWidget
    
    [myfedora.plugins.apps.packagesnav.views]
    home =  myfedora.plugins.apps.packagesnav:PackagesNavWidget
    canvas = myfedora.plugins.apps.packagesnav:PackagesNavWidget
    
    [myfedora.plugins.apps.buildstable.views]
    canvas = myfedora.plugins.apps.buildstable:BuildsTableWidget
    
    [myfedora.plugins.apps.fedoraannounce.views]
    home = myfedora.plugins.apps.fedoraannounce:FedoraAnnounceHomeWidget
    canvas = myfedora.plugins.apps.fedoraannounce:FedoraAnnounceCanvasWidget
    
    [myfedora.plugins.apps.peoplealphalist.views]
    home = myfedora.plugins.apps.peoplealphalist:PeopleAlphaListWidget
    canvas = myfedora.plugins.apps.peoplealphalist:PeopleAlphaListWidget

    [myfedora.plugins.apps.useralerts.views]
    home = myfedora.plugins.apps.useralerts:UserAlertsWidget
    canvas = myfedora.plugins.apps.useralerts:UserAlertsWidget
    
    [myfedora.plugins.apps.tools.packageinfo.views]
    home = myfedora.plugins.apps.tools.packageinfo:PackageInfoToolWidget
    canvas = myfedora.plugins.apps.tools.packageinfo:PackageInfoToolWidget
    
    [myfedora.plugins.apps.tools.builds.views]
    home = myfedora.plugins.apps.tools.builds:BuildsToolWidget
    canvas = myfedora.plugins.apps.tools.builds:BuildsToolWidget
    
    [myfedora.plugins.apps.tools.helloworld.views] 
    home = myfedora.plugins.apps.tools.helloworld:HelloWorldToolWidget
    canvas = myfedora.plugins.apps.tools.helloworld:HelloWorldToolWidget
    
    [myfedora.plugins.apps.tools.searchall.views] 
    home = myfedora.plugins.apps.tools.searchall:SearchAllToolWidget
    canvas = myfedora.plugins.apps.tools.searchall:SearchAllToolWidget
    
    [myfedora.plugins.apps.tools.searchpackages.views] 
    home = myfedora.plugins.apps.tools.searchpackages:SearchPackagesToolWidget
    canvas = myfedora.plugins.apps.tools.searchpackages:SearchPackagesToolWidget

    [myfedora.plugins.apps.tools.searchpeople.views] 
    home = myfedora.plugins.apps.tools.searchpeople:SearchPeopleToolWidget
    canvas = myfedora.plugins.apps.tools.searchpeople:SearchPeopleToolWidget
    
    [myfedora.plugins.apps.tools.fedoramemberships.views]
    home = myfedora.plugins.apps.tools.fedoramemberships:FedoraMembershipsToolWidget
    canvas = myfedora.plugins.apps.tools.fedoramemberships:FedoraMembershipsToolWidget

    [myfedora.plugins.apps.updates.views]
    home = myfedora.plugins.apps.updates:FedoraUpdatesWidget
    canvas = myfedora.plugins.apps.updates:FedoraUpdatesWidget

    [paste.paster_create_template]
    moksha-app = myfedora.pastetemplate:MokshaAppTemplate

    """,
)
