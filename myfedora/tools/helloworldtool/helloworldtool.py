from myfedora.plugin import Tool
from turbogears import expose

class HelloWorldTool(Tool):
    def __init__(self, parent_resource):
        Tool.__init__(self, parent_resource,
                                   'Hello World',
                                   'helloworld',
                                   'Prints out hello',
                                   'Take the data and prints out hello data',
                                   ['test'],
                                   ['test'])

    @expose()
    def default(self, resource, data=''):
        return "Hello " + data + " how do you like resource " + resource
