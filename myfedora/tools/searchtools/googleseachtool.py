from myfedora.plugin import Tool
from turbogears import expose

class MainSearchTool(Tool):
    def __init__(self, parent_resource):
        Tool.__init__(self, parent_resource,
                                   'Google',
                                   'google',
                                   'Goole search',
                                   '''Uses google to perform a search''',
                                   ['search'],
                                   [])

    @expose(template='myfedora.tools.searchtools.templates.index', allow_json=True)
    def index(self, search_string='', **kwargs):
        result = self.get_parent_resource().get_template_globals(search_string)

        return result

    # need to do this in order to get back non html formatted data 
    def _raw_results(self, search_string):
        parent = self.get_parent_resource()        
        result_hash = {'header': self.get_display_name(),
                       'url': parent.cat_tool_url(self.get_id(),
                                                  search_string),
                       'iframe_url': 'http://www.google.com/search?hl=en&q=' + search_string + '&btnG=Search',
                       'items':[]
                      }

        search_results = [result_hash]
       
        return search_results

    @expose(template='myfedora.tools.searchtools.templates.results', allow_json=True)
    def results(self, search_string=''):
        parent = self.get_parent_resource()
        result = parent.get_template_globals(search_string)
        result.update(self._raw_results())

        return result 
