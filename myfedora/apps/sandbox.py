from tw.api import Widget, js_function
from tw.jquery import JQuery,jquery_js
from myfedora.lib.app_factory import AppFactory

class SandboxApp(AppFactory):
    entry_name = 'sandbox'

class SandboxHomeWidget(Widget):
    params = ['url', 'script']

    template = 'genshi:myfedora.apps.templates.sandbox'
    javascript = [jquery_js]
    html = ''
    url = None

    def update_params(self, d):
        super(SandboxHomeWidget, self).update_params(d)
        
        if d.get('url', None):
            self.add_call("""$('document').ready(
                                 function() {
                                     frames['%s_sandbox_placeholder'].location.href="%s";
                                 }
                             );""" % (d['id'], d['url'])
                         )
        else:
            src="http://gmodules.com/ig/ifr?url=http://www.canbuffi.de/gadgets/clock/clock.xml&amp;up_title=Clock%20%26%20Date&amp;up_time_format=0&amp;up_seconds=1&amp;up_date_format=0&amp;up_dayofweek=1&amp;up_offset_hours=-4&amp;up_offset_minutes=&amp;up_daylight=0&amp;up_color=red&amp;synd=open&amp;w=320&amp;h=120&amp;title=__UP_title__&amp;lang=en&amp;country=ALL&amp;border=%23ffffff%7C3px%2C1px+solid+%23999999&amp;output=html" 
            self.add_call("""$(document).ready(
                                 function() {
                                     if_id = '%(id)s_sandbox_placeholder';
                                     ifr = frames[if_id];
                                     ifr.location.href="%(src)s";
                                     ifr.id = if_id;
                                     ifr.name = if_id;
                                 }
                             );"""  % {'id':d['id'], 'src':src}
                         )


        return d

