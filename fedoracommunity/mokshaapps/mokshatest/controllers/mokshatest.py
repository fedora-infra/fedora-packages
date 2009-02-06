from moksha.lib.base import Controller
from tg import expose

class RootController(Controller):

    @expose('mako:fedoracommunity.mokshaapps.mokshatest.templates.mokshatest')
    def index(self):
        return {}
