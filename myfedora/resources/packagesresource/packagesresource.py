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

        self.set_master_template("master")

    def get_template_globals(self, package, **kwargs):
        result = Resource.get_template_globals(self)
        dict = {}

        tool_list = self.get_tool_list()

        tool_urls = []
        for tool in tool_list:
            tool_urls.append((self.get_tool_url(tool.get_id(), package), 
                              tool.get_display_name())) 

        result.update({'tool_urls': tool_urls,
                       'package': package})
        return result

    def set_tool_route(self, route_map, tool):
        tool_id = tool.get_id()
        resource_id = self.get_id()
        controller_id = self._namespace_id(tool_id)

        if tool.is_default():
            route_map.connect(self.url(resource_id), 
                              contoller = controller_id)

        r = self._route_cat(self.url(resource_id),
                            ':package',
                            tool_id)

        route_map.connect(r, 
                          controller=controller_id, 
                          package='_all')

        return controller_id
