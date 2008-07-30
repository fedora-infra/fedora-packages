from myfedora.lib.app_factory import ResourceViewAppFactory
from myfedora.controllers.resourceview import ResourceViewController

class PeopleViewController(ResourceViewController):
    pass

class PeopleViewApp(ResourceViewAppFactory):
    entry_name = 'people'
    display_name = 'People'
    controller = PeopleViewController


