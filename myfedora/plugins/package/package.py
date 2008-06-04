from tg import expose
from myfedora.lib.base import BaseController

class PackageController(BaseController):

    @expose('myfedora.plugins.package.templates.package')
    def index(self, *args, **kwargs):
        print "PackageController.index!!!"
