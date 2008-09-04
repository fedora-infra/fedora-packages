from myfedora.widgets.resourceview import ToolWidget
from fedora.tg.client import BaseClient
from myfedora.lib.app_factory import AppFactory

class ProfileInfoToolApp(AppFactory):
    entry_name = "tools.profileinfo"

class ProfileInfoToolWidget(ToolWidget):
    template = 'genshi:myfedora.plugins.apps.tools.templates.profileinfo'
    display_name = "Info"

    def update_params(self, d):
        super(ProfileInfoToolWidget, self).update_params(d)
        
        return d