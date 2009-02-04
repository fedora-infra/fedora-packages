from moksha.lib.base import BaseController
from moksha.lib.helpers import MokshaApp
from tg import expose, tmpl_context
from fedoracommunity.widgets import SubTabbedContainer

class TabbedNav(SubTabbedContainer):
    tabs= (MokshaApp('Info', 'fedoracommunity.profile.info/me'),
           MokshaApp('Memberships', 'fedoracommunity.profile.memberships/me'),
           MokshaApp('Packages Maintenance', 'fedoracommunity.profile.packagemaint/me'),
          )

class RootController(BaseController):
    def __init__(self):
        self.widget = TabbedNav('myprofilenav')

    @expose('mako:moksha.templates.widget')
    def index(self):
        tmpl_context.widget = self.widget
        return {'options':{}}
