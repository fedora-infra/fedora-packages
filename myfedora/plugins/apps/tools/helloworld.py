from myfedora.widgets.resourceview import ToolWidget

class HelloWorldWidget(ToolWidget):
    template = 'genshi:myfedora.plugins.apps.tools.templates.hello'
    display_name = "Hello World Test"
