from moksha.lib.base import Controller
from moksha.lib.helpers import MokshaApp, Category
from moksha.api.widgets.containers import DashboardContainer
from tg import expose, tmpl_context
from fedoracommunity.widgets import SubTabbedContainer

class NameTabbedNav(SubTabbedContainer):
    tabs = (MokshaApp('Info', 'fedoracommunity.profile.info/name/'),
            MokshaApp('Memberships', 'fedoracommunity.profile.memberships/name/'),
            MokshaApp('Packages Maintenance', 'fedoracommunity.profile.packagemaint/name/'),
           )

class IndexDashboard(DashboardContainer):
    layout = [Category('left-content-col', MokshaApp('All People', 'fedoracommunity.peoplelist'))]
    engine_name = 'mako'
    template = """
<div id="${id}">
  <H2>People</H2>
  % for c in layout:
    ${applist_widget(category=c)}
  % endfor
</div>
"""

class RootController(Controller):
    def __init__(self):
        self.name_widget = NameTabbedNav('namepeoplenav')
        self.index_widget = IndexDashboard('indexdashboard')

    @expose('mako:moksha.templates.widget')
    def index(self):
        tmpl_context.widget = self.index_widget
        return {'options':{}}

    @expose('mako:moksha.templates.widget')
    def name(self, username):
        tmpl_context.widget = self.name_widget
        return {'options':{'username': username}}