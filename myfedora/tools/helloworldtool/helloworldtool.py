from myfedora.plugin import Tool
from turbogears import expose
import random

class HelloWorldTool(Tool):
    def __init__(self, parent_resource):
        Tool.__init__(self, parent_resource,
                                   'Hello World',
                                   'helloworld',
                                   'Prints out hello',
                                   'Take the data and prints out hello data',
                                   ['test'],
                                   ['test'])

    @expose(template='myfedora.tools.helloworldtool.templates.helloworld', allow_json=True)
    def default(self, data=''):
        result = self.get_parent_resource().get_template_globals()
       
        result.update({'data': data}) 
        return result
