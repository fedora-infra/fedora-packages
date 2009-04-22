from moksha.api.widgets.containers import TabbedContainer
from moksha.api.widgets.containers.dashboardcontainer import applist_widget
from moksha.lib.helpers import Category

class ExtraContentTabbedContainer(TabbedContainer):
    params = ['applist_widget', 'sidebar_apps', 'header_apps']
    applist_widget = applist_widget
    sidebar_apps = []
    header_apps = []

    def update_params(self, d):
        d['sidebar_apps'] = Category('sidebar-apps', self.sidebar_apps).process(d)
        d['header_apps'] = Category('header-apps', self.header_apps).process(d)

        super(ExtraContentTabbedContainer, self).update_params(d)

class SubTabbedContainer(TabbedContainer):
    template = 'mako:fedoracommunity.widgets.templates.subtabbedcontainer'
    passPathRemainder = True