from myfedora.lib.app_factory import ResourceViewAppFactory
from myfedora.controllers.resourceview import ResourceViewController

from tw.jquery import jquery_js, jQuery
from tw.api import Widget, JSLink, js_function, js_callback

from tg import expose

import pylons

class PackagesViewController(ResourceViewController):
    @expose('genshi:myfedora.plugins.resourceviews.templates.packagesindex')
    def index(self):
        return {}

class PackagesViewApp(ResourceViewAppFactory):
    entry_name = 'packages'
    display_name = 'Package Maintenance'
    controller = PackagesViewController

    def update_params(self, d):
        d['package'] = d.get('data_key', None)

        super(PackagesViewApp, self).update_params(d)
