from toscawidgets.api import WidgetBunch
import pylons

class WidgetFactory(WidgetBunch):    
    def render(self, data):
        rendered_widgets = ""
        for id, widget_data in data.items():
            widget_id = widget_data['widget_id']
            widget = self[widget_id]
            rendered_widgets += widget.render(id=widget_id, 
                                              widget_data['app_data'])

        return rendered_widgets

class AppBundle(object):
    def __init__(self, id):
        self.id = id
        self.apps = []
        self._counter = 0

    @property("counter")
    def read_counter(self):
        c = self._counter
        self._counter += 1

        return c

    def add(self, app_factory):
        self.apps.append(app_factory)
    
    def get_app_id(self, app):
        if app.config_id:
            return app.config_id
        else:
            return app.name + '_' + id + '_' + str(counter)

    def compose(self):
        formatted_data = {}

        wf = WidgetFactory()
        for a in self.apps:
            wf.add(a.get_widget())
            formatted_data[self.get_app_id(app)] = app.get_data()
           
        pylons.tmpl_context.widget_factory = 
            pylons.tmpl_context.get('widget_factory', {})

        pylons.tmpl_context.widget_factory[self.id] = wf

        return formatted_data
