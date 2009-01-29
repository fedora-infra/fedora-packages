from moksha.lib.base import BaseController
from moksha.api.widgets import ContextAwareWidget, Grid
from tg import expose, tmpl_context
from fedoracommunity.widgets.widgets import GlobalResourceInjectionWidget

class BuildsGrid(Grid, ContextAwareWidget):
    template='mako:fedoracommunity.mokshaapps.builds.templates.table_widget'

builds_grid = BuildsGrid('builds_table')

class RootController(BaseController):

    # do something for index, this should be the container stuff
    @expose()
    def index(self):
        w = GlobalResourceInjectionWidget()
        w.register_resources()
        return {}
    
    @expose('mako:fedoracommunity.mokshaapps.builds.templates.table')
    def table(self, uid="", rows_per_page=5, filters={}):
        ''' table handler
        
        This handler displays the main table by itself
        '''
        
        if isinstance(rows_per_page, basestring):
            rows_per_page = int(rows_per_page)
        
        tmpl_context.widget = builds_grid
        return {'filters': filters, 'uid':uid, 'rows_per_page':rows_per_page}