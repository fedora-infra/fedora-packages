from myfedora.lib.app_factory import ResourceViewAppFactory
from myfedora.controllers.resourceview import ResourceViewController
from myfedora.widgets.resourceview import ResourceViewWidget

from tw.jquery import jquery_js, jQuery
from tw.api import Widget, JSLink, js_function, js_callback

from tg import expose

import pylons

class PackagesViewController(ResourceViewController):
    @expose('genshi:myfedora.plugins.resourceviews.templates.packagesindex')
    def index(self, **kw):
        return {}
    
class PackagesViewWidget(ResourceViewWidget):
    data_keys=['data_key', 'package']

class PackagesViewApp(ResourceViewAppFactory):
    entry_name = 'packages'
    display_name = 'Package Maintenance'
    controller = PackagesViewController
    widget_class = PackagesViewWidget