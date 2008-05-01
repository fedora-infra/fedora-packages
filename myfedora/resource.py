import turbogears

from tool import ToolLoadException

class Resource(object):
    """
    This is the starting point for MyFedora plugins. A resource is any abstract 
    grouping such as "packages", "people" and "projects" which contain tools
    for viewing and manipulating data within the resource's context.

    Classes which inherit from this class should be placed in the resources/ 
    directory.
    """

    def __init__(self, display_name, 
                 mount_point, 
                 short_description, 
                 long_description):
        """
        Constructor Parameters:

            display_name -- how this resource should be displayed in a link
            mount_point -- where in the path hierachy to mount this resource,
                           relitive to the myfedora base path
            short_description -- a one line description of the resource
            long_description -- a more complete description of the resource
        """
        self.display_name = display_name
        self.mount_point = mount_point
        self.short_description = short_description
        self.long_description = long_description

        self._my_tools = {} # a hash of tools registered with this resource
        self._auth_level_required = False # right now just True or False but can be
                                  # expanded to include levels of authentication
        self._active = True # if False then don't register
        self._tool_order = [] # list of tool ids identifying precidence of 
                              # display
        self._icon = None # if an icon is present it can be used in the web page

    def get_display_name(self):
        """Returns -- the display name for output in a web page"""
        return self.display_name

    def get_mount_point(self):
        """Returns -- the relitive url mount point"""
        return self.mount_point

    def get_short_description(self):
        """Returns -- the one line description of this resource """
        return self.short_description

    def get_long_description(self):
        """Returns -- the more detailed description of this resource """
        return self.long_description

    def is_active(self):
        """Returns -- wether or not this resource is active"""
        return self._is_active

    def get_requires_auth(self):
        """Returns -- if this resource requires the user be authenticated.
        This is just the first implementation.  Later implementations will
        sync with FAS in order to have more finely grained control over access
        """
        if not self._auth_level_required:
            return False
    
        return True

    def get_tool_list(self):
        """Returns -- a user ordered list of registered tools. 
        Tools not given an order by the user are ordered alphabetically 
        """
        ordered_tool_list = []
        tool_dict = self._my_tools.copy()

        # get tools in the user defined tool order
        for tool_id in self._tool_order:
            tool = tool_dict.get(tool_id, None)
            if tool:
                ordered_tool_list.append(tool)

            del tool_dict[tool_id]

        # go over the remaining tools and sort them alphabetically
        remaining_tools = tool_dict.keys()
        remaining_tools.sort(key=str.tolower)
        for tool_id in remaining_tools:
            tool = tool_dict[tool_id]
            ordered_tool_list.append(tool)

        return ordered_tool_list

    def register_tool(self, tool_cls):
        """registers a tool with this resource  
        
        This is only used by the myfedora loader.  If the tool is inactive
        we do not register it.

        Parameter:

            tool_cls -- the class of the tool to register

        Raises:

            ToolLoadException -- raised when two or more of the same tools
                                 are loaded since tools should be unique 
                                 per resource 
        """
        tool = tool_cls(self)

        # don't register if inactive
        if not tool.is_active():
            return

        tool_id = tool.get_id()
        if (self._my_tools.get(tool_id)):
            raise ToolLoadException("Tool %s registered twice in the %s resource" % (tool_id, self.get_display_name()))

        self._my_tools[tool_id] = tool

    def set_auth_required(self, required):
        """Sets if this resource can only be used by users who are logged in
        
        Parameter:
            
            required -- True or False
        """
        self._auth_level_required = required

    def set_active(self, active):
        """Sets if this resource should be loaded
        
        Parameter:
            
            active -- True or False
        """
        self._is_active = active

    def set_icon_url(self, icon_url):
        """Sets an icon url that can be used in web pages

        Parameter:
            
            icon_url -- a relitive or complete URL to the icon
        """
        self._icon_url = icon_url

    def set_tool_route(self, route_map, tool):
        """Pure virtual method that needs to be overridden by the derived class

        Parameters:
        
            route_map -- a route map to add the match to
            tool -- the tool in which we are creating the route for

        see http://routes.groovie.org/ for more information on Python routes
        """
        raise NotImplementedError('A subclass of myfedora.Resource needs to override the get_route method')

    def _route_cat(self, *args):
        result = ''
        for arg in args:
            result += arg
            if arg.strip()[-1] != '/':
                result += '/'

        return result

    def _namespace_id(self, id):
        return self.get_mount_point() + '.' + id

    def url(self, source_url):
        """Sanitize a URL so we are pointing to the correct mount
        e.g. if myfedora is mounted on /myfedora URL('resource') will return
        '/myfedora/resource'

        Parameter:

            source_url -- the url to sanitize
        """
        return turbogears.url(source_url)
