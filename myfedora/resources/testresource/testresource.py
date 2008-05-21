from myfedora.plugin import Resource

class TestResource(Resource):
    """Test is an example resource"""

    def __init__(self):
        Resource.__init__(self, 'Test',
                                'test',
                                'Test resource',
                                '''Test resource for testing out the loaders
                                and acting as an example
                                ''')

        self.set_master_template('master')

    def get_template_globals(self, *args, **kwargs):
        result = Resource.get_template_globals(self, *args, **kwargs)
       
        data = kwargs.get('data', '')
        
        # get the list of registered tools to send to the template
        tool_list = self.get_tool_list()

        tool_urls = []
        for tool in tool_list:
            tool_urls.append((self.get_tool_url(tool.get_id(), data),
                              tool.get_display_name()))

        # set some global data the template can use
        result.update({'tool_urls': tool_urls,
                       'resource_name': self.get_id()
                      })

        return result

    def set_tool_route(self, route_map, tool):
        tool_id = tool.get_id()
        resource_id = self.get_id()
        controller_id = self._namespace_id(tool_id)
        if tool.is_default():
            route_map.connect(self.url(resource_id), 
                              contoller = controller_id,
                              resource = self)

        r = self._route_cat(self.url(resource_id),
                            ':data',
                            tool_id)

        route_map.connect(r, 
                          controller = controller_id, 
                          data = '')

        return controller_id
