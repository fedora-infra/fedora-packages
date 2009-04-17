from moksha.lib.base import Controller
from moksha.lib.helpers import MokshaApp, MokshaWidget, Category, Not, not_anonymous
from moksha.api.widgets.containers import DashboardContainer
from tg import expose, tmpl_context
from fedoracommunity.widgets import SubTabbedContainer

class NameTabbedNav(SubTabbedContainer):
    tabs = (MokshaApp('Info', 'fedoracommunity.people',
                      params={'username':None}),
            MokshaApp('Memberships', 'fedoracommunity.people/memberships',
                      params={'username':None}),
            MokshaApp('Package Maintenance', 'fedoracommunity.people/packagemaint',
                      params={'username':None}),
           )

class PeopleBrowserDashboard(DashboardContainer):
    layout = [Category('left-content-col',
                       (MokshaApp('All People', 'fedoracommunity.people/table', auth=not_anonymous()),
                        MokshaWidget('Login to browse a list of Fedora Users', 'fedoracommunity.login', auth=Not(not_anonymous()))
                       )
                      )]
    template = 'mako:fedoracommunity.mokshaapps.peopleresource.templates.people_browser'

name_widget = NameTabbedNav('namepeoplenav')
people_browser_widget = PeopleBrowserDashboard('peoplebrowserdashboard')

class RootController(Controller):
    @expose('mako:moksha.templates.widget')
    def index(self, username=None):
        if username:
            return self.name(username)

        tmpl_context.widget = people_browser_widget
        return {'options':{}}

    @expose('mako:moksha.templates.widget')
    def name(self, username):
        tmpl_context.widget = name_widget
        return {'options':{'username': username}}