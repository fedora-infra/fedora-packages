from tg import expose, tmpl_context, validate
from formencode import validators

from moksha.lib.base import Controller
from moksha.api.widgets import ContextAwareWidget, Grid

class UpdatesGrid(Grid, ContextAwareWidget):
    template='mako:fedoracommunity.mokshaapps.updates.templates.table_widget'

updates_grid = UpdatesGrid('updates_table')

class RootController(Controller):

    # do something for index, this should be the container stuff
    @expose()
    def index(self):
        return {}

    @expose('mako:fedoracommunity.mokshaapps.updates.templates.table')
    @validate(validators={'rows_per_page': validators.Int()})
    def table(self, uid="", rows_per_page=5, filters={}):
        ''' table handler

        This handler displays the main table by itself
        '''
        tmpl_context.widget = updates_grid
        return {'filters': filters, 'uid': uid, 'rows_per_page': rows_per_page}
