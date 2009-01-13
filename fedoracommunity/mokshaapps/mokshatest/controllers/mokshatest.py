from moksha.lib.base import BaseController
from tg import expose
from myfedora.widgets.widgets import GlobalResourceInjectionWidget

class RootController(BaseController):

    @expose('mako:myfedora.mokshaapps.mokshatest.templates.mokshatest')
    def index(self):
        w = GlobalResourceInjectionWidget()
        w.register_resources()
        return {}