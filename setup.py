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
    builds = myfedora.plugins.tools.builds:BuildsToolWidget
    hello = myfedora.plugins.tools.helloworld:HelloWorldWidget

    [myfedora.plugins.resourceviews.people.tools]
    builds = myfedora.plugins.tools.builds:BuildsToolWidget

    [myfedora.widgets.home]
    rss = myfedora.widgets:FedoraPeopleWidget
    helloworld = myfedora.widgets:HelloWorldWidget

    [myfedora.widgets.canvas]
    rss = myfedora.widgets:FedoraPeopleWidget
    helloworld = myfedora.widgets:HelloWorldWidget
    
    [myfedora.widgets.profile]
    rss = myfedora.widgets:FedoraPeopleWidget
    helloworld = myfedora.widgets:HelloWorldWidget

    [myfedora.widgets.preview]
    rss = myfedora.widgets:FedoraPeopleWidget
    helloworld = myfedora.widgets:HelloWorldWidget

    [myfedora.widgets.config]
    rss = myfedora.widgets:FedoraPeopleWidget
    helloworld = myfedora.widgets:HelloWorldWidget

    [myfedora.data]
    rss = myfedora.widgets:FedoraPeopleData

    [myfedora.apps]
    rss = myfedora.widgets:FedoraPeopleApp
    helloworld = myfedora.widgets:HelloWorldApp
    """,
)
