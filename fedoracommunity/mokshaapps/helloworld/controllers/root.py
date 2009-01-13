from moksha.lib.base import BaseController
from tg import expose
from myfedora.widgets.widgets import GlobalResourceInjectionWidget

class RootController(BaseController):

    @expose('mako:myfedora.mokshaapps.helloworld.templates.index')
    def index(self):
        return dict(world='World')

    @expose('mako:myfedora.mokshaapps.helloworld.templates.index')
    def test(self):
        return dict(world='Test')
    
    @expose('mako:myfedora.mokshaapps.helloworld.templates.index')
    def name(self, name='Nobody'):
        return dict(world=name)