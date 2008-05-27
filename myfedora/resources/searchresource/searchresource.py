from myfedora.plugin import Resource

class SearchResource(Resource):
    """The Search Resource allows for different search tools to reside under on
    roof.     
    """

    def __init__(self):
        Resource.__init__(self, 'Search',
                                'search',
                                'Tools to help search Fedora\'s many resources',
                                '''The Search Resource is the home for
                                tools which provide results for a search string.
                                Tools registered for this resource will recive
                                a search_string parameter.
                                ''')

        self.set_master_template("master")
        self._tool_order = ['main', 'packages']

    def get_template_globals(self, search_string, **kwargs):
        result = Resource.get_template_globals(self)
        dict = {}

        tool_list = self.get_tool_list()

        tool_urls = []
        for tool in tool_list:
            tool_urls.append((self.cat_tool_url(tool.get_id(), search_string), 
                             tool.get_display_name(),
                             tool.get_id()))

        result.update({'tool_urls': tool_urls,
                       'search_string': search_string})
        return result

    def set_tool_route(self, route_map, tool):
        tool_id = tool.get_id()
        resource_id = self.get_id()
        controller_id = self._namespace_id(tool_id)
        
        if tool.is_default():
            route_map.connect(self.url(resource_id), 
                              controller = controller_id)

        r = self._route_cat(self.url(resource_id),
                            tool_id,
                            ':search_string')

        route_map.connect(r, 
                          controller=tool_id, 
                          search_string=None)

        return controller_id
