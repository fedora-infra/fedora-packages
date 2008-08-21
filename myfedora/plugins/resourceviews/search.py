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

class SearchViewApp(ResourceViewAppFactory):
    entry_name = 'search'
    display_name = 'Search'
    controller = SearchViewController
    widget_class = SearchViewWidget
    
    def update_params(self, d):
        super(SearchViewApp, self).update_params(d)
        

    