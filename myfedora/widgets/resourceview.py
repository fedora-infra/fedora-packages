from tw.api import Widget
from tw.jquery import jquery_js
class ResourceViewWidget(Widget):
    params = ['']
    template = 'genshi:myfedora.plugins.resourceviews.templates.view'
    javascript = [jquery_js]
    data = None
    event_cb = None

    def update_params(self, d):
        if d.get('tool', None):
            active_tool = self[d['tool']]
            d[active_tool]['active'] = True 
             
        super(ResourceViewWidget, self).update_params(d)

        return d
