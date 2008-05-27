from myfedora.plugin import Resource

class PeopleResource(Resource):
    """People works on Fedora developers as a resource set.  All tools are
    given a person's login id as their routing data.    
    """

    def __init__(self):
        Resource.__init__(self, 'Fedora Developers',
                                'people',
                                'Tools to help maintain Fedora developers',
                                '''The Fedora people resource is the home for
                                tools which work on developer datasets.  Tools
                                registered for this resource must accept a
                                person parameter.  This will be the id of 
                                a developer which can be used to query various 
                                data sources for information relevant to the 
                                tool
                                ''')

        self.set_master_template("master")

    def get_template_globals(self, person, **kwargs):
        result = Resource.get_template_globals(self)
        dict = {}

        tool_list = self.get_tool_list()

        tool_urls = []
        for tool in tool_list:
            tool_urls.append((self.get_tool_url(tool.get_id(), person), 
                              tool.get_display_name())) 

        result.update({'tool_urls': tool_urls,
                       'person': person})
        return result

    def set_tool_route(self, route_map, tool):
        tool_id = tool.get_id()
        resource_id = self.get_id()
        controller_id = self._namespace_id(tool_id)

        if tool.is_default():
            route_map.connect(self.url(resource_id), 
                              contoller = controller_id)

        r = self._route_cat(self.url(resource_id),
                            ':person',
                            tool_id)

        route_map.connect(r, 
                          controller=controller_id, 
                          person='_all')

        return controller_id
