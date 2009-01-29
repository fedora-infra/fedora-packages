from moksha.lib.base import BaseController
from tg import expose

class RootController(BaseController):

    @expose('mako:fedoracommunity.mokshaapps.helloworld.templates.index')
    def index(self):
        return dict(world='World')

    @expose('mako:fedoracommunity.mokshaapps.helloworld.templates.index')
    def test(self):
        return dict(world='Test')
    
    @expose('mako:fedoracommunity.mokshaapps.helloworld.templates.index')
    def name(self, name='Nobody'):
        return dict(world=name)