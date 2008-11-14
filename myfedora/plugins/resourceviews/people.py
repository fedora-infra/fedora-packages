from myfedora.lib.app_factory import ResourceViewAppFactory
from myfedora.controllers.resourceview import ResourceViewController
from myfedora.widgets.resourceview import ResourceViewWidget
from myfedora.lib.appbundle import AppBundle

from tg import expose

import pylons

class PeopleViewController(ResourceViewController):
    @expose('mako:/plugins/resourceviews/templates/peopleindex.html')
    def index(self, **kw):
        result = super(PeopleViewController, self).index(**kw)
        leftcol_apps = AppBundle("leftcol")
        search = kw.get('search', 'a*')
        app = pylons.g.apps['peoplealphalist'](None, 
                                              None, 
                                              None, 
                                              'Canvas',
                                               search=search)
        leftcol_apps.add(app)
        result.update({'leftcol_apps': leftcol_apps.serialize_apps(pylons.tmpl_context.w)})
        
        return result 

class PeopleViewWidget(ResourceViewWidget):
    data_keys=['data_key', 'person']
    template='mako:/myfedora/plugins/resourceviews/templates/peopleview.html'

class PeopleViewApp(ResourceViewAppFactory):
    entry_name = 'people'
    display_name = 'People'
    controller = PeopleViewController
    widget_class = PeopleViewWidget
    requires_auth = True


