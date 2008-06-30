from myfedora.widgets.resourceview import ToolWidget

class HelloWorldWidget(ToolWidget):
    template = 'genshi:myfedora.plugins.tools.templates.hello'
    display_name = "Hello World Test"
