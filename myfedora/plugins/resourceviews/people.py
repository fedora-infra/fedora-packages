from myfedora.lib.app_factory import ResourceViewAppFactory
from myfedora.controllers.resourceview import ResourceViewController
from myfedora.widgets.resourceview import ResourceViewWidget

from tg import expose

class PeopleViewController(ResourceViewController):
    @expose('genshi:myfedora.plugins.resourceviews.templates.peopleindex')
    def index(self, **kw):
        return {}

class PeopleViewWidget(ResourceViewWidget):
    data_keys=['data_key', 'person']
    template='genshi:myfedora.plugins.resourceviews.templates.peopleview'

class PeopleViewApp(ResourceViewAppFactory):
    entry_name = 'people'
    display_name = 'People'
    controller = PeopleViewController
    widget_class = PeopleViewWidget
    requires_auth = True


