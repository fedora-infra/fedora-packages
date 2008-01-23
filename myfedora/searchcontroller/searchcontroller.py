from turbogears import controllers, expose
from turbogears import redirect

from searchplugins import PackageSearch

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

        ps = PackageSearch()
        list = ps.search(search)
        dict['search_results'] = list

        return dict
