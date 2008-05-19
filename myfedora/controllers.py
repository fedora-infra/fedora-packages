import os
import re
import logging
import sys

from searchcontroller import SearchController
from mfquery.querycontroller import QueryController

from datetime import timedelta, datetime
from turbogears import controllers, expose, flash, url
from turbogears import identity, redirect
from cherrypy import request, response, HTTPRedirect, NotFound

from routes import *

from myfedora.plugin import Resource, Tool

# route mapper
m = Mapper()

log = logging.getLogger("myfedora.controllers")

class Root(controllers.RootController):
    search = SearchController()
    mfquery = QueryController()

    def __init__(self):
        self.base_re = re.compile( r'^(?P<protocol>[a-zA-Z]+)://(?P<host>.*)' )
        
        # Change the controllers here to the controllers in your app:
        self.controllers = {
              'main': self
            }
        
        # Here you need to add your own routes (http://routes.groovie.org/manual.html)
        self._register_resources()
        self._register_tools()
        self._register_tool_routes()
         
        m.create_regs(self.controllers.keys())
        
    def _register_resources(self):
        """Dynamically import resources in the resources directory"""
        self.resources = {}

        resource_dir = os.path.join('myfedora', 'resources')
        top_dirlist = os.listdir(resource_dir)
        for td in top_dirlist:
            plugin_resource_dir = os.path.join(resource_dir, td)
            if os.path.isdir(plugin_resource_dir):
                resource_dirlist = os.listdir(plugin_resource_dir)
                for f in resource_dirlist:
                    if f.endswith('.py'):
                        __import__("myfedora.resources." + td + '.' + f[:-3],
                                   None,
                                   None,[],0)

        classes = Resource.__subclasses__()

        for c in classes:
            r = c()
            self.resources[r.get_id()] = r

    def _register_tools(self):
        """Dynamically import tools in the tools directory"""
        self.tools = {}

        tools_dir = os.path.join('myfedora','tools')
        tools_dir_files = os.listdir(tools_dir)
        for tf in tools_dir_files:
            plugin_tool_dir = os.path.join(tools_dir, tf)
            if os.path.isdir(plugin_tool_dir):
                tool_files = os.listdir(plugin_tool_dir)
                for f in tool_files:
                    if f.endswith('.py'):
                        __import__("myfedora.tools." + tf + '.' + f[:-3],
                                   None,None,[],0)

        classes = Tool.__subclasses__()

        for c in classes:
            # instantiate once so we can get the mount point 
            # and resource ids
            t = c(None)

            if t.is_active():
                tool_id = t.get_id()
                self.tools[tool_id] = c 
                resource_ids = t.get_resource_ids()

                for id in resource_ids:
                    # pass in the class so that the resource can instantiate 
                    # its own instance of the tool
                    r = self.resources[id]
                    r.register_tool(c)
                    

    def _register_tool_routes(self):
        for resource in self.resources.values():
            
            for tool in resource.get_tool_list():
                controller_key = resource.set_tool_route(m, tool)
                self.controllers[controller_key] = tool

    def redirect(self, url):
        # Recreated this function as the cherrypy one is depreciated
        raise HTTPRedirect(turbogears.url(url), 302)

    @expose(template='myfedora.templates.index', allow_json=True)
    def index(self):
        ### FIXME:
        # This doesn't quite work because we don't recurse into the container
        # to find the javascript entries for the widgets.  Probably need a
        # new container class that extracts javascript and css properties from
        # the widgets.
        widgets = ([], [], [])
        # use defaults
        widgets[LEFT].append(FedoraPeopleWidget('people1'))
        widgets[RIGHT].append(FedoraUpdatesWidget('updates1'))
        widgets[RIGHT].append(RawhideBugsWidget('rawhide1'))
        if not identity.current.anonymous:
            userWidgets = identity.current.user.widgets
            if userWidgets:
                # FIXME: need to instantiate the class
                # in widget_config.widgetClass
                for widget_config in userWidgets:
                    widget_class = getattr(widget_config.widgetClass, '__new__')
                    widgets[widget_config.config['display']['column']] \
                        [widget_config.config['display']['row']] = \
                        widget_class(widget_config.widgetId)
            else:
                for widgetCol in widgets:
                    for widget in widgetCol:
                        widget_config = widget.save()
                        identity.current.user.addWidgetConfig(widget_config.id)

        return {
            'widgets': widgets,
        }


    @expose(template="myfedora.templates.login")
    def login(self, forward_url=None, previous_url=None, *args, **kw):

        if not identity.current.anonymous \
            and identity.was_login_attempted() \
            and not identity.get_identity_errors():
            raise redirect(forward_url)

        forward_url=None
        previous_url= request.path

        if identity.was_login_attempted():
            msg=_("The credentials you supplied were not correct or "
                   "did not grant access to this resource.")
        elif identity.get_identity_errors():
            msg=_("You must provide your credentials before accessing "
                   "this resource.")
        else:
            msg=_("Please log in.")
            forward_url= request.headers.get("Referer", "/")

        response.status=403
        return dict(message=msg, previous_url=previous_url, logging_in=True,
                    original_parameters=request.params,
                    forward_url=forward_url)

    @expose()
    def logout(self):
        identity.current.logout()
        raise redirect("/")

    @expose()
    def default(self, *args, **kwargs):

        base = request.base
        d = self.base_re.match( base ).groupdict()
        host = d[ 'host' ]
        proto = d[ 'protocol' ]
        path = request.path

        con = request_config()
        con.mapper = m # the Routes Mapper object
        con.host = host
        con.protocol = proto
        con.redirect = self.redirect
        con.mapper_dict = m.match( path )

        if con.mapper_dict:
            c = con.mapper_dict.pop( 'controller' )
            controller = self.controllers[c]
            action = con.mapper_dict.pop( 'action', 'index' )
            try:
                meth = getattr(controller, action, getattr(controller, 'default'))
            except AttributeError:
                raise NotFound( path )
            kwargs.update( con.mapper_dict )
            return meth( **kwargs )

        raise NotFound( path )


# vim:ts=4:sw=4:et:

