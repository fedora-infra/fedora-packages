from tw.api import Widget
from tw.jquery import jquery_js

class ToolWidget(Widget):
    params = ['active']

    active = False
    javascript = [jquery_js]
    data = None
    event_cb = None

    def __init__(self, id, *args, **kwargs):
        super(ToolWidget, self).__init__(id, *args, **kwargs)
        if not self.display_name:
            self.display_name = id

class BuildToolWidget(ToolWidget):
    template = 'genshi:myfedora.plugins.tools.templates.builds'
    display_name = "Builds"

    def update_params(self, d):
        print d

        super(ToolWidget, self).update_params(d)
        return d
