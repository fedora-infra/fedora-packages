from moksha.lib.base import Controller
from tg import expose

class RootController(Controller):

    @expose('mako:fedoracommunity.mokshaapps.helloworld.templates.index')
    def index(self):
        return dict(world='World')

    @expose('mako:fedoracommunity.mokshaapps.helloworld.templates.index')
    def test(self):
        return dict(world='Test')
    
    @expose('mako:fedoracommunity.mokshaapps.helloworld.templates.index')
    def name(self, name='Nobody'):
        return dict(world=name)