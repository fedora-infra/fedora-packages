import re
import logging
import feedparser

from testcontroller import TestController
from packagecontroller import PackageController

from datetime import timedelta, datetime
from turbogears import controllers, expose, flash
from turbogears import identity, redirect
from cherrypy import request, response

from toscawidgets.api import Widget as TWWidget
from myfedora.model import WidgetConfig

log = logging.getLogger("myfedora.controllers")

urlDataMap = {}
LEFT, MIDDLE, RIGHT = range(3)


class Widget(TWWidget):
    config = {
        'display' : None,
        'widget' : None,
    }
    widgetId = None
    engine_name='genshi'
    
    def __init__(self, widgetId):
        self.widgetId = widgetId

        if not identity.current.anonymous:
            self.config.display = WidgetConfig(widgetId, 'display')
            self.config.widget = WidgetConfig(widgetId, 'widget')

class RSSData(list):
    """
    Eventually:
    - ability for widgets to specify filters?  so we don't have to hardcode our 
      regex in this widget
        - filters = ([field_to_filter, regex, results_field]) ??
    """
    def __init__(self, url, pollInterval):
        self.url = url
        self.pollInterval = pollInterval
        self.lastChange = datetime.utcnow()
        self.lastPoll = datetime.utcnow()
        self.refresh(force=True)

    def refresh(self, force=False):
        if not force and (datetime.utcnow() - self.lastPoll) < self.pollInterval:
            log.debug("Skipping refresh")
            return
        log.debug("Refreshing entries")
        newEntries = []
        regex = re.compile('<img src="(.*)" alt="" />')
        feed = feedparser.parse(self.url)
        for entry in feed['entries'][:5]: # FIXME: use config info
            newEntries.append({
                'link'  : entry['link'],
                'title' : entry['title'],
                'image' : regex.match(entry['summary']).group(1)
            })
        for entry in range(0, len(newEntries)):
            if newEntries[entry].link != self[entry].link:
                self[:]
                self.extend(newEntries)
                self.lastChange = datetime.utcnow()
                break
        self.lastPoll = datetime.utcnow()

class RSSWidget(Widget):
    template = 'myfedora.templates.rsswidget'
    pollInterval = timedelta(minutes=15)
    params = ["title", "entries", "maxEntries"]
    entries = 5

    def __init__(self, widgetId, title = None, url = None, maxEntries = None):
        super(RSSWidget, self).__init__(widgetId)
        self.url = url or self.url
        self.title = title or self.title
        self.entries = maxEntries or self.entries
        try:
            self.entries = urlDataMap[self.url]
        except KeyError:
            urlDataMap[self.url] = RSSData(self.url, self.pollInterval)
            self.entries = urlDataMap[self.url]
        self.entries.refresh()


    def __json__(self):
        return {'widgetId': self.widgetId, 'url':self.url, 'entries': self.entries}


class FedoraPeopleWidget(RSSWidget):
    url = 'http://planet.fedoraproject.org/rss20.xml'
    title = 'Fedora People'

class Root(controllers.RootController):
    # /packages/ is used for the package views
    packages = PackageController()
    test = TestController()

    @expose(template='myfedora.templates.index', allow_json=True)
    def index(self):
        widgets = ([], [], [])
        if identity.current.anonymous:
            # use defaults
            widgets[LEFT].append(FedoraPeopleWidget('people1'))
        else:
            ### FIXME:
            # figure out what widgets user wants to display
            # instantiate widgets with custom configuration
            pass
        return {
            'widgets': widgets
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
