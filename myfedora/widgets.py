import re
import time
import feedparser
import simplejson

from Comet import comet

from model import FedoraPeopleData

from turbogears import url
from turbogears.widgets import Widget
from turbogears.widgets.base import JSLink, CSSLink

from toscawidgets.api import Widget as TWWidget
from toscawidgets.api import JSLink as TWJSLink
from toscawidgets.api import CSSLink as TWCSSLink

class LocalJSLink(JSLink):
    """ 
    Link to local Javascript files 
    """ 
    def update_params(self, d):
        super(JSLink, self).update_params(d)
        d["link"] = url(self.name)

class LocalTWJSLink(TWJSLink):
    def update_params(self, d):
        super(TWJSLink, self).update_params(d)
        d["link"] = url(self.filename)

class LocalTWCSSLink(TWCSSLink):
    def update_params(self, d):
        super(TWCSSLink, self).update_params(d)
        d["link"] = url(self.filename)

class LocalCSSLink(CSSLink):
    """ 
    Link to local Javascript files 
    """ 
    def update_params(self, d):
        super(CSSLink, self).update_params(d)
        d["link"] = url(self.name)

class FedoraPeopleTWWidget(TWWidget):
    javascript = [ LocalTWJSLink(modname='widgets',
        filename='/static/js/fedorawidgets.js'),
            LocalTWJSLink(modname='widgets',
                filename='/static/js/fedorapeople-tgwidget.js')]
    css = [ LocalTWCSSLink(modname='widgets',
        filename='/static/css/fedorapeople.css')]
    template = 'widgets.fedorawidgets.twpeople'
    engine_name = 'genshi'
    params = ["entries", "widgetId", "widgetUrl", "max_length"]

    def __init__(self, widgetId=None, parent=None, children=[], widgetUrl=None, max_length=3, **kw):
        super(FedoraPeopleTWWidget, self).__init__(widgetId, parent, children, **kw)
        self.entries = []
        regex = re.compile('<img src="(.*)" alt="" />')
        feed = feedparser.parse('http://planet.fedoraproject.org/rss20.xml')
        for entry in feed['entries']:
            self.entries.append({
                'link'  : entry['link'],
                'title' : entry['title'],
                'image' : regex.match(entry['summary']).group(1)
            })

    def update_params(self, params):
        super(FedoraPeopleTWWidget, self).update_params(params)
        regex = re.compile('<img src="(.*)" alt="" />')
        feed = feedparser.parse('http://planet.fedoraproject.org/rss20.xml')
        for entry in feed['entries']:
            self.entries.append({
                'link'  : entry['link'],
                'title' : entry['title'],
                'image' : regex.match(entry['summary']).group(1)
            })

    def __json__(self):
        return {'id': self.widgetId, 'entries': self.entries}

class FedoraPeopleWidget(Widget):
    javascript = [ LocalJSLink('widgets', '/static/js/fedorawidgets.js'),
            LocalJSLink('widgets', '/static/js/fedorapeople-tgwidget.js')]
    css = [ LocalCSSLink('widgets', '/static/css/fedorapeople.css')]
    # We can place the widget code in its own template if we choose.
    #template = 'widgets.fedorawidgets.fedorapeople'
    template = """
       <table xmlns:py="http://purl.org/kid/ns#"
         class="widget FedoraPeopleWidget" py:attrs="{'id': widgetId}">
          <tr py:for="entry in entries[:5]">
            <td><img src="${entry['image']}" height="32" width="32"/></td>
            <td><a href="${entry['link']}">${entry['title']}</a></td>
          </tr>
        </table>
    """
    params = ["entries","widgetId", "widgetUrl"]

    def __init__(self, widgetUrl, widgetId=None):
        self.widgetId = widgetId
        self.widgetUrl = widgetUrl
        self.entries = []
        regex = re.compile('<img src="(.*)" alt="" />')
        feed = feedparser.parse('http://planet.fedoraproject.org/rss20.xml')
        for entry in feed['entries']:
            self.entries.append({
                'link'  : entry['link'],
                'title' : entry['title'],
                'image' : regex.match(entry['summary']).group(1)
            })

    def __json__(self):
        return {'id': self.widgetId, 'entries': self.entries}


class CometWidget(TWWidget):
    """ Parent class for our comet-based widgets.

    When subclassing, supply a javascript 'handler', which is executed with
    each piece of data that is pushed from our server through our comet tunnel.
    You also need to provide a callback method, 'generator', which will get
    called by an XMLHttpRequest from our client.  This parent class takes
    care of setting up the persistent comet tunnel.
    """
    template = 'widgets.templates.cometwidget'
    params = ["cb", "handler"]
    engine_name = 'genshi'

    def __init__(self):
        self.cb = url('/callback?widget=%s' % self.__class__.__name__)
        if not hasattr(self, 'handler'):
            raise NotImplementedError, "Missing javascript handler"

    def callback(self):
        """ Our data generator callback, executed by our clients XMLHttpRequest

        This method returns a comet generator back to CherryPy, which will then
        return a streaming response body back to our client.
        """
        return comet('text/plain')(self.generator)()

    @staticmethod
    def generator(self):
        """ A data generator called by the clients XMLHttpRequest.

        This method should yield data that will be sent back to the client
        asynchronously and handled by this widgets supplied javascript 'handler'
        """
        raise NotImplementedError

class FedoraPeople(CometWidget):
    """ A FedoraPeople comet widget.

    We supply a static data generator callback method that is executed by our
    client.  This callback returns a comet generator that allows us to stream
    content back to our client.  We then provide provide a javascript handler
    that will get executed asynchronously by the client with each piece of data
    that is pushed from the server through the comet tunnel.
    """
    handler = """
      function handler(evt){
        var entries = eval(evt.target.responseText);
        $.each(entries, function(i, entry){
          $("<div/>").hide().append(
          $("<img/>").attr("src", entry['image'])
            .attr("height", "32").attr("width", "32")
          ).append(
            $("<a/>").attr("href", entry['link']).text(entry['title'])
          ).prependTo("#data").slideDown();
        });
      }
    """

    @staticmethod
    def generator():
        data = FedoraPeopleData()
        for entry in data:
            try:
                yield simplejson.dumps([entry])
            except GeneratorExit:
                print "GeneratorExit!!"
                return
            time.sleep(1.5)
