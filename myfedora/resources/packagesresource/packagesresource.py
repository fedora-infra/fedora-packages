from myfedora.plugin import Resource

class PackagesResource(Resource):
    """Packages works on Fedora packages as a resource set.  All tools are
    given a package name as their routing data.    
    """

    def __init__(self):
        Resource.__init__(self, 'Fedora Packages',
                                'packages',
                                'Tools to help maintain Fedora packages',
                                '''The Fedora packages resource is the home for
                                tools which work on package datasets.  Tools
                                registered for this resource must accept a
                                package parameter.  This will be the package
                                name which can be used to query various data
                                sources for information relevant to the tool
                                ''')
    def set_tool_route(self, route_map, tool):
        tool_id = tool.get_id()
        resource_id = self.get_id()
        controller_id = self._namespace_id(tool_id)

        if tool.is_default():
            route_map.connect(self.url(resource_id), 
                              contoller = controller_id,
                              resource = resource_id)

        r = self._route_cat(self.url(resource_id),
                            ':package',
                            tool_id)

        route_map.connect(r, 
                          controller=self._namespace_id(tool.get_id()), 
                          package='_all',
                          resource=resource_id)

        return controller_id
