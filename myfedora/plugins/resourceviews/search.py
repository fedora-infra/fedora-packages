from myfedora.lib.app_factory import ResourceViewAppFactory
from myfedora.controllers.resourceview import ResourceViewController
from myfedora.widgets.resourceview import ResourceViewWidget

from tg import expose

import pylons

class SearchViewController(ResourceViewController):
    pass

class SearchViewWidget(ResourceViewWidget):
    template='genshi:myfedora.plugins.resourceviews.templates.searchview'
    data_keys=['data_key', 'search']
    
    def update_params(self, d):
        super(SearchViewWidget, self).update_params(d)
        search_children = []
        for c in self.children:
            key = c._id + '_checkbox'
            
            if d.get(key, None) == 'checked':
                search_children.append(c)
                
            if not search_children and d.get('data_key', None):
                # search all 
                search_children = d['visible_children']
                
        d['search_children'] = search_children

class SearchViewApp(ResourceViewAppFactory):
    entry_name = 'search'
    display_name = 'Search'
    display_overview = False
    controller = SearchViewController
    widget_class = SearchViewWidget