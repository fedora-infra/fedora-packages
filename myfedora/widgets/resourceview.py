from tw.api import Widget
from tw.jquery import jquery_js
from widgets import myfedora_ui_js
from widgets import myfedora_extensions_js
from pylons import tmpl_context, request
import tg

# use for now but figure out better way to add extra tabs
class DummyToolWidget(object):
    def __init__(self, _id, display_name):
        self._id = _id
        self.display_name = display_name 

class ResourceViewWidget(Widget):
    params = ['data_key']
    data_keys = ['data_key']
    template = 'genshi:myfedora.widgets.resourceview'
    display_overview = True
    
    javascript = [jquery_js]
    data = None
    event_cb = None
    
    def __init__(self, *args, **kw):
        do = kw.get('display_overview')
        if do is not None:
            self.display_overview = False
            del kw['display_overview']
        
        super(ResourceViewWidget, self).__init__(*args, **kw)
    
    def syncronize_data_keys(self, d, data_key):
        result = {}
        for dk in self.data_keys:
            result[dk] = data_key

        d.update(result)
        
        return result
                
    def get_data_key(self, d):
        data_key = None
        s = super(ResourceViewWidget, self)
        if getattr(s, 'get_data_key', None):
            data_key = s.get_data_key()

        if data_key:
            return data_key
        
        for dk in self.data_keys:
            data_key = d.get(dk, None)
            if data_key:
                return data_key
    
    def update_params(self, d):
        super(ResourceViewWidget, self).update_params(d)
        data_key = self.get_data_key(d)
        childargs = self.syncronize_data_keys(d, data_key)
        if d.get('tool', None):
            active_tool = self.children[d['tool']]
            if active_tool.requires_data_key and not data_key:
                return None
            
            d['active_child'] = active_tool
        else:
            active_child = None 
            for child in self.children:
                if not child.requires_data_key or data_key:
                    active_child = child
                    break
                
            if not active_child:
                return None
            
            d['active_child'] = active_child

        visible_children = []
        childurls = {}
        
        if data_key == None and self.display_overview:
            ov = DummyToolWidget('overview', 'Overview')
            visible_children = [ov]
            childurls = {ov._id: '/%s/' % tmpl_context.resource_view}
            
        for c in self.children:
            if c.requires_data_key and not data_key:
                continue
            
            if c.requires_auth and not tmpl_context.indentity:
                continue
             
            childargs.update({'resourceview': d['config']['widget_id']})
            
            d['child_args'][c.key] = childargs
            visible_children.append(c)
            
            path = request.environ['PATH_INFO']
            path_elements = path.split('/')
            path_count = len(path_elements) - path_elements.count('')
            if data_key and path_count > 2 :
                childurls[c._id] = tg.url("/%s/name/%s/%s" % (tmpl_context.resource_view,
                                                       data_key,
                                                       c._id)
                                         )
            else:
                childurls[c._id] = tg.url("/%s/%s" % (tmpl_context.resource_view,
                                                      c._id)
                                         )
            
        d['visible_children'] = visible_children
        d['childurls'] = childurls
        
        return d

class ToolWidget(Widget):
    params = ['active']

    active = False
    javascript = [jquery_js, myfedora_ui_js, myfedora_extensions_js]
    data = None
    event_cb = None
    requires_data_key = True
    requires_auth = False

    def __init__(self, id=None, *args, **kwargs):
        super(ToolWidget, self).__init__(id, *args, **kwargs)
