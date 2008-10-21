from myfedora.widgets.resourceview import ToolWidget
from fedora.client import BaseClient
from myfedora.lib.app_factory import AppFactory
from myfedora.lib.appbundle import AppBundle

import pylons

class ProfileInfoToolApp(AppFactory):
    entry_name = "tools.profileinfo"

class ProfileInfoToolWidget(ToolWidget):
    template = 'genshi:myfedora.plugins.apps.tools.templates.profileinfo'
    display_name = "Info"

    def update_params(self, d):
        super(ProfileInfoToolWidget, self).update_params(d)
        
        right_apps = AppBundle("rightcol")
        c = pylons.g.apps['useralerts']
        app = c(None, 
                view='Home')
        
        right_apps.add(app)
        

        d.update({'rightcol': right_apps.serialize_apps(pylons.tmpl_context.w)})
        
        return d