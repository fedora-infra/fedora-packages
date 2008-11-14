from myfedora.lib.app_factory import ResourceViewAppFactory
from myfedora.controllers.resourceview import ResourceViewController
from myfedora.widgets.resourceview import ResourceViewWidget

from tw.jquery import jquery_js, jQuery
from tw.api import Widget, JSLink, js_function, js_callback

from tg import expose

import pylons

class ProfileViewController(ResourceViewController):
    @expose('mako:/resourceviewcontainer.html')
    def default(self, *args, **kw):
        if pylons.tmpl_context.identity and pylons.tmpl_context.identity.get('person'):
            kw.update({'data_key': pylons.tmpl_context.identity['person']['username'],
                       'person': pylons.tmpl_context.identity['person']['username']})
        
        d = super(ProfileViewController, self).default(*args, **kw)

        return d
    
class ProfileViewWidget(ResourceViewWidget):
    template='mako:/myfedora/plugins/resourceviews/templates/profileview.html'
    params=['person']
    data_keys=['data_key', 'person']

class ProfileViewApp(ResourceViewAppFactory):
    entry_name = 'profile'
    widget_class = ProfileViewWidget
    display_name = 'My Profile'
    controller = ProfileViewController
    requires_auth = True
