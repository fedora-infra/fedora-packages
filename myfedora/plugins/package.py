from tg import expose
from myfedora.lib.base import BaseController

class PackageController(BaseController):

    @expose('genshi:package')
    def index(self, *args, **kwargs):
        print "PackageController.index!!!"
        return dict(data="Booyah")
