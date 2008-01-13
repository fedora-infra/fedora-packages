from turbogears import controllers, expose
from turbogears import redirect

class SearchController(controllers.Controller):
    @expose(template='myfedora.templates.search.index')
    def index(self):
        dict = {}
        return dict

    @expose(template='myfedora.templates.search.results')
    def default(self, *args, **kw):
        dict = {}
        
        search = kw.get('search', None)
        if not search:
            dict['tg_template'] = 'myfedora.templates.search.index'            
        else:
            dict['search'] = search

        return dict
