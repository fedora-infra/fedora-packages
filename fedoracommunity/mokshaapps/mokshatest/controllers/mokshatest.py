from moksha.lib.base import BaseController
from tg import expose
from fedoracommunity.widgets.widgets import GlobalResourceInjectionWidget

class RootController(BaseController):

    @expose('mako:fedoracommunity.mokshaapps.mokshatest.templates.mokshatest')
    def index(self):
        w = GlobalResourceInjectionWidget()
        w.register_resources()
        return {}