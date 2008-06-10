from myfedora.lib.base import Controller
import pylons

class BaseViewController(Controller):
    def __init__(self):
        super(BaseViewController, self).__init__()
        self.view = '' 

    def get_view(self):
        return self.view

    def set_view(self, view):
        self.view = view

    def init_context():
        pylons.tmpl_context.w.content_view = self.view
