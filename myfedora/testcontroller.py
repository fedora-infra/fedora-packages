from turbogears import controllers, expose
from turbogears import redirect

class TestController(controllers.Controller):
    @expose(template='myfedora.templates.test')
    def index(self):
        dict = {}
        return dict

    @expose(template='myfedora.templates.test')
    def default(self, *args, **kw):
        dict = {}
        return dict 
