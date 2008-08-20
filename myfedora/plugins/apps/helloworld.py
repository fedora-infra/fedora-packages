from myfedora.lib.app_factory import AppFactory
from tg import url
from tw.api import Widget, JSLink, js_function, js_callback
from tw.jquery import jquery_js, jQuery

class HelloWorldApp(AppFactory):
    entry_name = 'helloworld'
                 
    def __init__(self, app_config_id, width=None, height=None, view='home', **kw):
        super(HelloWorldApp, self).__init__(app_config_id, 
            width, height, view, **kw)

    def get_data(self, force_refresh=False):
        data = super(HelloWorldApp, self).get_data(force_refresh)

        return data

class HelloWorldWidget(Widget):
   """ A sample widget for testing

   This widget says hello to whatever string resides in the hello_to parameter
   passed to it and then prints out its configuration.
   """
   params = ['hello_to']
   template = 'genshi:myfedora.plugins.apps.templates.helloworld'
   javascript = [jquery_js]
   data = None
   event_cb = None

   def update_params(self, d):
        super(HelloWorldWidget, self).update_params(d)
        d['greeting'] = 'Hello' 
        return d
