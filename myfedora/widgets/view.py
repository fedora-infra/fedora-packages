from tw.api import Widget
from tw.jquery import jquery_js
class ViewWidget(Widget):
    params = ['']
    template = 'genshi:myfedora.plugins.views.templates.view'
    javascript = [jquery_js]
    data = None
    event_cb = None

    def update_params(self, d):
        if d.get('tool', None):
            active_tool = self[d['tool']]
            d[active_tool]['active'] = True 
             
        super(ViewWidget, self).update_params(d)

        return d
