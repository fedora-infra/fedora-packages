from myfedora.plugins.views.view import BaseViewController
#from myfedora.widgets import ViewWidget

class PeopleViewController(BaseViewController):
    def __init__(self):
        super(PeopleViewController, self).__init__()
        #self.set_view(ViewWidget('people'))

    def default(self, *args, **kwargs):
       pass 
        
