from myfedora.plugins.views.view import BaseViewController
#from myfedora.widgets import ViewWidget

class PackagesViewController(BaseViewController):
    def __init__(self):
        super(PackagesViewController, self).__init__()
        #self.set_view(ViewWidget('packages'))

    def default(self, *args, **kwargs):
       pass 
        
