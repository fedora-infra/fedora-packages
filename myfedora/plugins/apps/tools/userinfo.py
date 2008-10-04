from myfedora.widgets.resourceview import ToolWidget
from fedora.client import BaseClient
from myfedora.lib.app_factory import AppFactory
from myfedora.lib.proxy import FasClient

class UserInfoToolApp(AppFactory):
    entry_name = "tools.userinfo"

class UserInfoToolWidget(ToolWidget):
    template = 'genshi:myfedora.plugins.apps.tools.templates.userinfo'
    display_name = "Info"

    def update_params(self, d):
        super(UserInfoToolWidget, self).update_params(d)
        
        user = d['data_key']
        
        fc = FasClient()
        result = fc.get_user_info(user)     
        if not result:
            return {}

        p = result['person']
        
        d.update({'person': p})
        return d