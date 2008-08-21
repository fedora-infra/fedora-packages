from myfedora.widgets.resourceview import ToolWidget
from myfedora.lib.app_factory import AppFactory

class HelloWorldToolApp(AppFactory):
    entry_name = "tools.helloworld"

class HelloWorldToolWidget(ToolWidget):
    template = 'genshi:myfedora.plugins.apps.tools.templates.hello'
    display_name = "Hello World Test"
