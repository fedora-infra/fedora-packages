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

    def set_tool_route(self, route_map, tool):
        tool_id = tool.get_id()
        resource_id = self.get_id()
        controller_id = self._namespace_id(tool_id)
        if tool.is_default():
            route_map.connect(self.url(resource_id), 
                              contoller = controller_id,
                              resource = resource_id)

        r = self._route_cat(self.url(self.get_id()),
                            ':data',
                            tool_id)

        route_map.connect(r, 
                          controller = controller_id, 
                          data = '',
                          resource = resource_id)

        return controller_id
