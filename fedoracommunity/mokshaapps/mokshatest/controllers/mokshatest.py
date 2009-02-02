from moksha.lib.base import BaseController
from tg import expose

class RootController(BaseController):

    @expose('mako:fedoracommunity.mokshaapps.mokshatest.templates.mokshatest')
    def index(self):
        return {}
