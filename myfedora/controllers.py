import re
import logging
import feedparser

from testcontroller import TestController
from packagecontroller import PackageController

from datetime import timedelta, datetime
from turbogears import controllers, expose, flash, url
from turbogears import identity, redirect
from cherrypy import request, response

from toscawidgets.api import Widget
from toscawidgets.api import JSLink as TWJSLink

from myfedora.model import WidgetConfig

from sqlobject import SQLObjectNotFound
from sqlobject.dberrors import *

log = logging.getLogger("myfedora.controllers")

urlDataMap = {}
LEFT, MIDDLE, RIGHT = range(3)


class FedoraWidget(Widget):
    engine_name='genshi'
    
    def __new__(cls, widgetId, parent=None, children=[], **kw):
        obj = super(FedoraWidget, cls).__new__(cls, widgetId, parent, children, **kw)

        obj.config = {
                'display' : {},
                'widget' : {},
                }
        if not identity.current.anonymous:
            for configType in obj.config.keys():
                try:
                    obj.config[configType] = WidgetConfig.selectBy(
                        widgetId=obj.widgetId,
                        configType=configType).getOne().config
                except SQLObjectNotFound:
                    pass
        return obj

    def save(self):
        for configType in self.config.keys():
            try:
                WidgetConfig(widgetId=self.widgetId, configType=configType,
                    config=self.config[configType])
            except DuplicateEntryError:
                wc = WidgetConfig.selectBy(
                    widgetId=self.widgetId,
                    configType=configType).getOne().set(
                        config=self.config[configType])

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

class RSSWidget(FedoraWidget):
    javascript = [ LocalTWJSLink(modname='myfedora',
        filename='/static/js/fedorawidgets.js')]

    template = 'myfedora.templates.rsswidget'
    pollInterval = timedelta(minutes=15)
    params = ["widgetId", "url", "title", "entries", "maxEntries"]
    entries = None
    maxEntries = 5
    url = ''
    title = 'RSS Feed'

    def __new__(cls, widgetId, parent=None, children=[], title = None, url = None, maxEntries = None, **kw):
        obj = super(RSSWidget, cls).__new__(cls, widgetId, parent, children, **kw)
        obj.config['display']['title'] = title or cls.title
        obj.config['widget']['url'] = url or cls.url
        obj.config['widget']['maxEntries'] = maxEntries or cls.maxEntries
        try:
            obj.entries = urlDataMap[obj.config['widget']['url']]
        except KeyError:
            urlDataMap[obj.config['widget']['url']] = RSSData(obj.config['widget']['url'], cls.pollInterval)
            obj.entries = urlDataMap[obj.config['widget']['url']]
        obj.entries.refresh()
        return obj

    def __json__(self):
        return {'widgetId': self.widgetId,
            'url': self.config['widget']['url'],
            'entries': self.entries,
            'maxEntries': self.config['widget']['maxEntries']}

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
        print 'widgetId type:', type(widgetId)
        rss = RSSWidget(widgetId, title, url, maxEntries)
        return { 'widget':rss }

    @expose(template='myfedora.templates.widget', allow_json=True)
    def FedoraPeople(self, widgetId, **kwargs):
        '''Serve the FedoraPeopleWidget.'''
        fedorapeople = FedoraPeopleWidget(widgetId)
        return { 'widget':fedorapeople }

    @expose(template='myfedora.templates.widget', allow_json=True)
    def RawhideBugs(self, widgetId, **kwargs):
        '''Serve the FedoraPeopleWidget.'''
        rawhidebugs = RawhideBugs(widgetId)
        return { 'widget':rawhidebugs }

    @expose(template='myfedora.templates.widget', allow_json=True)
    def FedoraUpdates(self, widgetId, **kwargs):
        '''Serve the FedoraPeopleWidget.'''
        fedoraupdates = FedoraUpdatesWidget(widgetId)
        return { 'widget':fedoraupdates }

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
        # use defaults
        widgets[LEFT].append(FedoraPeopleWidget('people1'))
        widgets[RIGHT].append(FedoraUpdatesWidget('updates1'))
        widgets[RIGHT].append(RawhideBugsWidget('rawhide1'))
        if not identity.current.anonymous:
            userWidgets = identity.current.user.widgets
            if userWidgets:
                for widget in userWidgets:
                    widgets[widget.config['display']['column']] \
                        [widget.config['display']['row']] = \
                        widget.widgetClass(widget.widgetId)

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

# vim:ts=4:sw=4:et:

