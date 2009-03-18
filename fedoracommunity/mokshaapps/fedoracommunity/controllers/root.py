from moksha.lib.base import Controller, BaseController
from moksha.api.widgets.containers import TabbedContainer
from moksha.api.errorcodes import login_err

from tg import expose, tmpl_context, redirect, flash, url
from fedoracommunity.mokshaapps.login import login_widget

# Root for the whole fedora-community tree
class MainNav(TabbedContainer):
    template = 'mako:fedoracommunity.mokshaapps.fedoracommunity.templates.mainnav'
    config_key = 'fedoracommunity.mainnav.apps'

class RootController(BaseController):

    def __init__(self):
        self.mainnav_tab_widget = MainNav('main_nav_tabs', action="create");

    @expose('mako:fedoracommunity.mokshaapps.fedoracommunity.templates.index')
    def index(self, ec = None, **kwds):
        # FIXME: we won't always display the main nav
        tmpl_context.widget = self.mainnav_tab_widget

        return {'title': 'Fedora Community', 'options':kwds}

    @expose('mako:fedoracommunity.mokshaapps.fedoracommunity.templates.index')
    def login(self, came_from = '/', ec = None):
        tmpl_context.widget = login_widget

        if ec:
            err = None
            try:
                err = login_err(ec)
            except AttributeError, e:
                pass

            if err:
                flash(err)

        if '/logout_handler' in came_from:
            came_from = url('/')

        return {'title': 'Fedora Community Login',
                'options':{'came_from': came_from}}

    @expose('mako:fedoracommunity.mokshaapps.fedoracommunity.templates.index')
    def default(self, *args, **kwds):

        redirect('/', anchor='/'.join(args), params=kwds)
