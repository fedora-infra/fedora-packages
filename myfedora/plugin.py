import os
import sys
import genshi.template.plugin
import cherrypy
import turbogears
from turbogears import controllers

# to be used by module for figuring out template locations
_template_engine = genshi.template.plugin.MarkupTemplateEnginePlugin()


class ToolLoadException(Exception):
    pass

class Tool(controllers.Controller):
    """
    A tool is a web app for viewing or manipulating data.  For example Builds
    would be a tool for the package resource.  Tools are implemented as self
    contained TurboGears controllers.

    Classes which inherit from Tool should reside in the myfedora/tools 
    directory within it's own self contained directory structure as such:

    <toolname>/
	    __init__.py
            <classfiles>.py
            templates/
        	    <kid template>.html
            static/
         	    images/
		        js/
		        css/
    """
    
    def __init__(self, resource,
                 display_name, 
                 id, 
                 short_description, 
                 long_description,
                 resource_ids,
                 default_for):
        """
        Inheriting from this object requires you override the constructor to
        accept only the resource parameter and fill in the rest of the 
        parameters when calling the parent class constructor.

        Example:

            class FooTool(Tool):
                def __init__(self, resource):
                    Tool.__init__(self, resource, 
                                  'Foo', 
                                  'foo',
                                  'This is the foo tool',
                                  'This is the foo tool, an example tool',
                                  ['people', 'packages'],
                                  ['people'])

        Constructor Parameters:

            resource -- the resource object passed in when the tool is 
                        registered
            display_name -- how this tool should be displayed in a link
            id -- unique name to refer to this tool as in hashes and url paths
            short_description -- a one line description of the tool
            long_description -- a more complete description of the tool
            resource_ids -- a list of resources this tool understands
            default_for -- a list of resources this tool is the default for

        Raises:
            
            ToolLoadException -- raised if the resource is not listed in the
                                 resource ids
        """

        self._parent_resource = resource
        self._display_name = display_name
        self._id = id
        self._short_description = short_description 
        self._long_description = long_description
        self._resource_ids = resource_ids
        self._default_for = default_for
        self._is_default = False
        self._is_active = True

        if resource:
            resource_id = resource.get_id()
            if (not resource_id in resource_ids):
                raise ToolLoadException("Tool %s doesn't understand how to deal with the %s resource" % (id, resource_id)) 

            if resource_id in default_for:
                self._is_default = True

    def is_default(self):
        """Returns -- if the tool is the default for its parent resource"""
        return self._is_default

    def get_parent_resource(self):
        """Returns -- the resource object the tool is registered with"""
        return self._parent_resource
    
    def get_display_name(self):
        """Returns -- the display name for output in a web page"""
        return self._display_name

    def get_id(self):
        """Returns -- the unique id"""
        return self._id
        
    def get_short_description(self):
        """Returns -- a short description of the tool"""
        return self._short_description
        
    def get_long_description(self):
        """Returns -- the longer description of the tool"""
        return self._long_description
    
    def get_resource_ids(self):
        """Returns -- a list of resource ids this tool understands"""
        return self._resource_ids

    def get_default_for(self):
        """Returns -- a list of resource ids this tool is the default for"""
        return self._default_for
   
    def is_active(self):
        """Returns -- wether or not this resource is active"""
        return self._is_active

    def set_active(self, is_active):
        """sets wether or not this resource is active
        
        Parameters:

            is_active -- enables or disables this tool
        """
        self._is_active = is_active

    @classmethod
    def local_template(cls, template_name):
        """Transforms the template_name into a fully qualified file path
        for refrencing templates within the local template directory

        Parameters:

            template_name -- the local template name 
                             (without the file extention)
            
        Returns -- a fully qualified path to the template
        """

        # use a traceback hack to find the calling file
        # we are always local to the calling file
        f = sys._getframe(1)

        dir = os.path.dirname(f.f_code.co_filename)

        # FIXME: we need to add the .html but genshi has config options to 
        #        set the file extention which is expected
        # FIXME: deal with templates in sub directories by swapping period
        #        delimiters for file delimiters 
        file = os.path.join(dir, 'templates', template_name + '.html') 
       
        return file
         
class Resource(object):
    """
    This is the starting point for MyFedora plugins. A resource is any abstract 
    grouping such as "packages", "people" and "projects" which contain tools
    for viewing and manipulating data within the resource's context.

    Classes which inherit from this class should be placed in the resources/ 
    directory.
    """

    def __init__(self, display_name, 
                 id, 
                 short_description, 
                 long_description):
        """
        Constructor Parameters:

            display_name -- how this resource should be displayed in a link
            id -- unique identifier and where in the path hierachy to mount 
                  this resource
            short_description -- a one line description of the resource
            long_description -- a more complete description of the resource
        """
        self._display_name = display_name
        self._id = id
        self._short_description = short_description
        self._long_description = long_description

        self._my_tools = {} # a hash of tools registered with this resource
        self._auth_level_required = False # right now just True or False but can be
                                  # expanded to include levels of authentication
        self._active = True # if False then don't register
        self._tool_order = [] # list of tool ids identifying precidence of 
                              # display
        self._icon = None # if an icon is present it can be used in the web page

        main_module = self.__module__.rsplit('.', 1)[0]

        self._template_namespace = main_module + ".templates"
        self._master_template = None 

    def get_master_template(self):
        """Returns -- the fully qualified master template for this resourcei
                      or None if not set
        """
        if self._master_template:
            file = _template_engine.load_template(self._master_template).filename
            return file

        return None

    def get_display_name(self):
        """Returns -- the display name for output in a web page"""
        return self._display_name

    def get_id(self):
        """Returns -- the unique id"""
        return self._id

    def get_short_description(self):
        """Returns -- the one line description of this resource """
        return self._short_description

    def get_long_description(self):
        """Returns -- the more detailed description of this resource """
        return self._long_description

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

    def cat_tool_url(self, *args):
        """creates a tg url santized link by concatinating the base URL
        for the resource to the string args
        
        Paramerters:
            
            *args -- a list of strings to be concatinated as elements in a path

        Returns -- the tg url sanitized link of all the concatinated elements
        """

        url = '/' + self.get_id()

        for a in args:
            url += '/' + a

        return turbogears.url(url)
     
    def get_tool_url(self, tool, data=None):
        """gets the tg url sanitized link to the requested tool
        
        Parameters:
            
            tool -- the tool's id we wish to link to
            data -- the data pointer for data we are working on

        Returns -- the tg url sanitized link to the requested tool
        """
        
        elements = []
        if data:
            elements.append(data)

        elements.append(tool)

        return self.cat_tool_url(*elements)

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
        remaining_tools.sort(key=str.lower)
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

    def set_master_template(self, name):
        """Set's the master template which can be used by tools to show
        a unified UI for the resource

        Parameters:
        
            name - the name of the template relitive to the resource's 
                   template directory
             
        """
        self._master_template = self._template_namespace + "." + name


    def get_template_globals(self, *args, **kwargs):
        """Method that can be over ridden to provide various data to the 
        tool's template

        Standard data:

            myfedora.resource -- this object
            myfedora.current_url -- your current url

        Parameters:

            args -- all the arguments passed to the tool's controller which

            kwargs -- all the keyword arguments sent to the tool's controller

        Returns -- a hash of data
        """
        return {'myfedora' :
                 {'resource': self,
                  'current_url': cherrypy.request.path
                 }
               }

    def set_tool_route(self, mapper, tool):
        """Pure virtual method that needs to be overridden by the derived class

        Parameters:
        
            mapper -- the route map we are modifying
            tool -- the tool in which we are creating the route for

        Returns -- the namespaced tool id 
                   (i.e. self._namespace_id(tool.get_id())

        see http://routes.groovie.org/ for more information on Python routes
        """
        raise NotImplementedError('A subclass of myfedora.Resource of type %s needs to override the set_tool_route method' % (str(type(self))))

    def _route_cat(self, *args):
        result = ''
        for arg in args:
            result += arg
            if arg.strip()[-1] != '/':
                result += '/'

        return result

    def _namespace_id(self, id):
        return self.get_id() + '.' + id

    def url(self, source_url):
        """Sanitize a URL so we are pointing to the correct mount
        e.g. if myfedora is mounted on /myfedora URL('resource') will return
        '/myfedora/resource'

        Parameter:

            source_url -- the url to sanitize
        """
        return turbogears.url(source_url)
