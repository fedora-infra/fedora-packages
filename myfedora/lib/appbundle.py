from tw.api import WidgetBunch
import pylons
from myfedora.lib.utils import pretty_print_array

class AppBundle(object):
    def __init__(self, id):
        self.id = id
        self.apps = []
        self._counter = 0

    def read_counter(self):
        c = self._counter
        self._counter += 1

        return c

    def add(self, app_factory):
        self.apps.append(app_factory)
    
    def get_app_uid(self, app):
        if app.config_id:
            return app.config_id
        else:
            return app.entry_name + '_' + self.id + '_' + str(self.read_counter())

    def serialize_apps(self, widget_bundle):
        formatted_data = []
        for a in self.apps:
            data = a.get_data()
            data['config']['uid'] = self.get_app_uid(a)
            formatted_data.append(data)

            w = a.get_widget()
            widget_bundle.append(w)

        return formatted_data
