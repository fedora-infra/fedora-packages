from tw.api import Widget
from myfedora.lib.app_factory import AppFactory

class PlaceholderApp(AppFactory):
    entry_name = 'placeholder'

class PlaceholderCanvasWidget(Widget):
    template = 'genshi:myfedora.apps.templates.placeholder_canvas'

    def update_params(self, d):
        super(PlaceholderCanvasWidget, self).update_params(d)
        
        if not 'placeholder_label' in d:
            d['placeholder_label'] = 'Undefined Placeholder'
        
        return d
    
class PlaceholderHomeWidget(PlaceholderCanvasWidget):
    template = 'genshi:myfedora.apps.templates.placeholder_home'
