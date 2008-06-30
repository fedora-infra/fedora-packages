from tg import url
from tw.api import Widget, JSLink, js_function, js_callback
from tw.jquery import jquery_js, jQuery
from myfedora.streams import RSSDataStream
from myfedora.lib.app_factory import AppFactory

orbited_js = JSLink(link='http://localhost:8000/_/orbited.js')
rsswidget_js = JSLink(link='/javascript/rsswidget.js')

class RSSWidget(Widget):
    """ A generic RSS widget.

    This Widget is able to stream data using comet to the user.  This means,
    that once the widget is rendered, it will automatically open a persistent
    connect back to the server where data will be pushed asynchronously.

    This widget uses jQuery to populate and animate new item creation.
    """
    params = ['name', 'entries', 'id']
    template = 'genshi:myfedora.templates.rsswidget'
    javascript=[orbited_js, jquery_js, rsswidget_js]
    include_dynamic_js_calls = True
    data = None # A DataStream, or... ?
    event_cb = None # a js_callback that handles new items

    def update_params(self, d):
        """ TODO:
        get the data feed name and user, and pass it to widget_connect ?
        allow for widgets to supply their own event_cb
        """
        super(RSSWidget, self).update_params(d)
        user = 'bobvila'
        event_cb = js_callback("""function(data) {
            $.each(data, function(i, entry){
              $("<div/>").hide().append(
                $("<img/>").attr("src", entry["image"])
                  .attr("height", "32").attr("width", "32")
                ).append(
                  $("<a/>").attr("href", entry["link"]).text(entry["title"])
                ).prependTo("#%s_data").slideDown();
              });
            }""" % self.id)
        self.add_call(js_function('widget_connect')(user,self.data.id,event_cb))

    def __str__(self):
        return "<%s %s>" % (self.__class__.__name__, self.id)


class FedoraPeopleData(RSSDataStream):
    url = 'http://planet.fedoraproject.org/rss20.xml'
    id = 'fedorapeople'

class FedoraPeopleApp(AppFactory):
    entry_name = 'rss'
    def __init__(self, app_config_id, width=None, height=None, view='Home', **kw):
        super(FedoraPeopleApp, self).__init__(app_config_id, width, height, view, **kw)
        self.rss_stream = FedoraPeopleData()

    def get_data(self, force_refresh=False):
        data = super(FedoraPeopleApp, self).get_data(force_refresh)
        data['rss-stream'] = FedoraPeopleData()
        return data

class FedoraPeopleWidget(RSSWidget):
    name = 'Fedora People'
    authors = ['Luke Macken <lmacken@redhat.com>']
    description = 'A streaming Fedora People widget'
    data = FedoraPeopleData
