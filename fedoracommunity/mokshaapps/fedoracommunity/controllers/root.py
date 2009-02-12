from moksha.lib.base import Controller, BaseController
from moksha.api.widgets.containers import TabbedContainer
from tg import expose, tmpl_context, redirect
from tw.jquery.ui_tabs import JQueryUITabs
from tw.core import CSSLink
from pylons import config

# Root for the whole fedora-community tree
class MainNav(TabbedContainer):
    template = 'mako:fedoracommunity.mokshaapps.fedoracommunity.templates.mainnav'
    config_key = 'fedoracommunity.mainnav.apps'

class RootController(BaseController):

    def __init__(self):
        self.mainnav_tab_widget = MainNav('main_nav_tabs', action="create");

    @expose('mako:fedoracommunity.mokshaapps.fedoracommunity.templates.index')
    def index(self):
        # FIXME: we won't always display the main nav
        tmpl_context.widget = self.mainnav_tab_widget

        return {'title': 'Fedora Community'}

    @expose('mako:fedoracommunity.mokshaapps.fedoracommunity.templates.index')
    def default(self, *args, **kwds):
        redirect('/#' + '/'.join(args), **kwds)