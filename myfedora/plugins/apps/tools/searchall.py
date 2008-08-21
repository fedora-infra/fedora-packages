from searchbase import SearchBaseWidget
from fedora.tg.client import BaseClient
import time
import tg

# sort based on weight, each element
def weighted_sort(a, b):
    result = 0
    a_weight = a['weight']
    b_weight = b['weight']
    
    result = -cmp(a_weight, b_weight)

    return result

class SearchAllToolWidget(SearchBaseWidget):
    params=['search_string', 'results']
    template = 'genshi:myfedora.plugins.apps.tools.templates.searchall'
    display_name = 'All'
    
    def search(self, search_terms, timeout_in_seconds=-1):
        weighted_pkg_list = []
        for child in self.parent.children:
            if child != self:
                weighted_pkg_list.extend(child.search(search_terms))
              
        weighted_pkg_list.sort(weighted_sort)
    
        return weighted_pkg_list
    
    
    
    