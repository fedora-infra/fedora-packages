from myfedora.widgets.resourceview import ToolWidget

class SearchBaseWidget(ToolWidget):
    params=['data_key']
    
    template = 'genshi:myfedora.plugins.apps.tools.templates.searchall'
    display_name = 'All'
    requires_data_key=False
    
    def search(self, search_terms, timeout_in_seconds=5):
        raise NotImplementedError('The search method must be implemented by the child')
    
    def update_params(self, d):
        super(SearchBaseWidget, self).update_params(d)
        results = d.get('results', [])
        
        search_string = d.get('data_key', None)
        
        print search_string

        if search_string:
            results = self.search(search_string)
        
        d['results'] = results
        
        widgets = {}
        for child in self.parent.children:
            widgets[child.id] = child
        
        d['widgets'] = widgets
        
        return d