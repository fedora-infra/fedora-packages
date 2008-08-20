from tw.api import Widget
from tw.jquery import jquery_js
from widgets import myfedora_ui_js
from widgets import myfedora_extentions_js

class ResourceViewWidget(Widget):
    params = ['display_name']
    template = 'genshi:myfedora.templates.resourceview'
    javascript = [jquery_js]
    data = None
    event_cb = None

    def update_params(self, d):
        super(ResourceViewWidget, self).update_params(d)
        if d.get('tool', None):
            active_tool = self.children[d['tool']]
            if active_tool.requires_data_key:
                return None
            
            d['active_child'] = active_tool
        else:
            active_child = None 
            for child in self.children:
                if not child.requires_data_key:
                    active_child = child
                    break
                
            if not active_child:
                return None
            
            d['active_child'] = active_child
         
        visible_children = []
        data_key = d['data_key']   
        for c in self.children:
            if c.requires_data_key and not data_key:
                continue
                
            d['child_args'][c.key] = \
                dict(resourceview = d['config']['widget_id'],
                     data_key = data_key) 
            
            visible_children.append(c)
            
        d['visible_children'] = visible_children
        
        return d

class ToolWidget(Widget):
    params = ['active']

    active = False
    javascript = [jquery_js, myfedora_ui_js, myfedora_extentions_js]
    data = None
    event_cb = None
    requires_data_key = True

    def __init__(self, id, *args, **kwargs):
        super(ToolWidget, self).__init__(id, *args, **kwargs)
        if not self.display_name:
            self.display_name = id
