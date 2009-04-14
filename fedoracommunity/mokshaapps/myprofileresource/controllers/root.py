from moksha.lib.base import Controller
from moksha.lib.helpers import MokshaApp
from tg import expose, tmpl_context
from fedoracommunity.widgets import SubTabbedContainer

class TabbedNav(SubTabbedContainer):
    tabs= (MokshaApp('Info', 'fedoracommunity.people',
                     params={'profile':True}),
           MokshaApp('Memberships', 'fedoracommunity.people/memberships',
                     params={'profile':True}),
           MokshaApp('Package Maintenance', 'fedoracommunity.people/packagemaint',
                     params={'profile': True}),
          )

class RootController(Controller):
    def __init__(self):
        self.widget = TabbedNav('myprofilenav')

    @expose('mako:moksha.templates.widget')
    def index(self):
        tmpl_context.widget = self.widget
        return {'options':{}}
