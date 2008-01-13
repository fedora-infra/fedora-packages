import re
import logging
import feedparser

from testcontroller import TestController
from packagecontroller import PackageController

from datetime import timedelta, datetime
from turbogears import controllers, expose, flash, url
from turbogears import identity, redirect
from cherrypy import request, response

from toscawidgets.api import Widget as TWWidget
from toscawidgets.api import JSLink as TWJSLink

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
    def __init__(self, feedUrl, pollInterval):
        self.url = feedUrl
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
        for entry in feed['entries']:
            newEntries.append({
                'link'  : entry['link'],
                'title' : entry['title']
            })
            if regex.match(entry['summary']):
                newEntries[-1]['image'] = regex.match(entry['summary']).group(1)
            
        changes = True
        if len(self) == len(newEntries):
            for entry in range(0, len(newEntries) - 1):
                if newEntries[entry]['link'] != self[entry]['link']:
                    break
            changes = False
            
        if changes:
            self[:]
            self.extend(newEntries)
            self.lastChange = datetime.utcnow()
            
        self.lastPoll = datetime.utcnow()

class LocalTWJSLink(TWJSLink):
    def update_params(self, d):
        super(TWJSLink, self).update_params(d)
        d["link"] = url(self.filename)

class RSSWidget(Widget):
    javascript = [ LocalTWJSLink(modname='myfedora',
        filename='/static/js/fedorawidgets.js')]

    template = 'myfedora.templates.rsswidget'
    pollInterval = timedelta(minutes=15)
    params = ["widgetId", "url", "title", "entries", "maxEntries"]

    def __init__(self, widgetId, title = None, url = None, maxEntries = None):
        super(RSSWidget, self).__init__(widgetId)
        self.url = url or self.url
        self.title = title or self.title
        self.maxEntries = maxEntries or 5
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

class RawhideBugsWidget(RSSWidget):
    url = 'https://bugzilla.redhat.com/buglist.cgi?bug_file_loc_type=allwordssubstr&bug_status=ASSIGNED&bug_status=MODIFIED&bug_status=NEEDINFO&bug_status=NEW&bugidtype=include&changedin=7&chfield=%5BBug%20creation%5D&chfieldto=Now&cust_facing_type=substring&devel_whiteboard_type=allwordssubstr&emailassigned_to1=1&emailassigned_to2=1&emailcc2=1&emailqa_contact2=1&emailreporter2=1&emailtype1=exact&emailtype2=exact&field0-0-0=noop&fixed_in_type=allwordssubstr&keywords_type=allwords&long_desc_type=substring&product=Fedora&qa_whiteboard_type=allwordssubstr&query_format=advanced&short_desc_type=allwordssubstr&status_whiteboard_type=allwordssubstr&type0-0-0=noop&version=rawhide&ctype=rss'
    title = 'Rawhide Bugs'

class FedoraUpdatesWidget(RSSWidget):
    url = 'https://admin.fedoraproject.org/updates/rss/rss2.0?status=stable'
    title = 'Fedora Updates'


class WidgetsController(controllers.Controller):
    '''Controller that serves an instance of a widget.

    This can be used to either:
    1. Serve a widget to another process (possibly over Comet)
    2. Serve data about a widget (once again, possibly over JSON)
    '''

    @expose(template='myfedora.templates.widget', allow_json=True)
    def RSS(self, widgetId, title = None, url = None, maxEntries = None, **kwargs):
        '''Serve the RSS Widget.'''
        print kwargs
        print RSSWidget
        print (dir (RSSWidget))
        rss = RSSWidget(widgetId, title, url, maxEntries)
        return { widget:rss }

    @expose(template='myfedora.templates.widget', allow_json=True)
    def FedoraPeople(self, widgetId):
        '''Serve the FedoraPeopleWidget.'''
        fedorapeople = FedoraPeopleWidget(widgetId)
        return { widget:fedorapeople }

    @expose(template='myfedora.templates.widget', allow_json=True)
    def RawhideBugs(self, widgetId):
        '''Serve the FedoraPeopleWidget.'''
        rawhidebugs = RawhideBugs(widgetId)
        return { widget:rawhidebugs }

    @expose(template='myfedora.templates.widget', allow_json=True)
    def FedoraUpdates(self, widgetId):
        '''Serve the FedoraPeopleWidget.'''
        fedoraupdates = FedoraUpdatesWidget(widgetId)
        return { widget:fedoraupdates }

class Root(controllers.RootController):
    # /packages/ is used for the package views
    packages = PackageController()
    test = TestController()
    widgets = WidgetsController()

    @expose(template='myfedora.templates.index', allow_json=True)
    def index(self):
        ### FIXME:
        # This doesn't quite work because we don't recurse into the container
        # to find the javascript entries for the widgets.  Probably need a
        # new container class that extracts javascript and css properties from
        # the widgets.
        widgets = ([], [], [])
        if identity.current.anonymous:
            # use defaults
            widgets[LEFT].append(FedoraPeopleWidget('people1'))
            widgets[RIGHT].append(FedoraUpdatesWidget('updates1'))
            widgets[RIGHT].append(RawhideBugsWidget('rawhide1'))
        else:
            ### FIXME:
            # figure out what widgets user wants to display
            # instantiate widgets with custom configuration
            pass

        return {
            'widgets': widgets,
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
