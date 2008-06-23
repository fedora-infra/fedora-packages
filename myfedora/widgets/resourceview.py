from tw.api import Widget
from tw.jquery import jquery_js

class ResourceViewWidget(Widget):
    params = ['display_name']
    template = 'genshi:myfedora.plugins.resourceviews.templates.view'
    javascript = [jquery_js]
    data = None
    event_cb = None

    def update_params(self, d):
        super(ResourceViewWidget, self).update_params(d)
        if d.get('tool', None):
            active_tool = self.children[d['tool']]
            d['active_child'] = active_tool
            
        for c in self.children:
            d['child_args'][c.key] = \
                dict(resourceview = d['config']['widget_id'],
                     data_key = d['data_key']) 
        return d

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
