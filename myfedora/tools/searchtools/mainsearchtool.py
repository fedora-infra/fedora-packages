from myfedora.plugin import Tool
from turbogears import expose

class MainSearchTool(Tool):
    def __init__(self, parent_resource):
        Tool.__init__(self, parent_resource,
                                   'All',
                                   'main',
                                   'Search resources',
                                   '''Uses all of the search tools to preform a 
                                    search and also hosts the main page''',
                                   ['search'],
                                   ['search'])

    @expose(template='myfedora.tools.searchtools.templates.index', allow_json=True)
    def index(self, search_string='', **kwargs):
        result = self.get_parent_resource().get_template_globals(search_string)

        return result

    @expose(template='myfedora.tools.searchtools.templates.results', 
    allow_json=True)
    def results(self, search_string='', filter=None):
        result = self.get_parent_resource().get_template_globals(search_string)
      
        search_results = []

        if filter == self.get_id():
            filter = None

        # fix me we should do this async in javascript
        for t in self.get_parent_resource().get_tool_list():
            if t == self:
                continue

            if not filter or t.get_id() == filter:
                search_results.extend(t._raw_results(search_string))
           
        result.update({'search_results': search_results,
                       'search_string': search_string}) 
        return result
