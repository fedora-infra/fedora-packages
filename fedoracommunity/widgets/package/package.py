import mako
import uuid
import moksha
import logging
import collections
import tw2.core as twc

from mako.template import Template
from moksha.api.connectors import get_connector

log = logging.getLogger(__name__)

class BugsWidget(twc.Widget):
    template = u"""Bugs
    dude
    """
    engine_name = 'mako'


class TabWidget(twc.Widget):
    template="mako:fedoracommunity.widgets.package.templates.tabs"
    base_url = twc.Param(default='/')
    args = twc.Param(default=None)
    kwds = twc.Param(default=None)
    tabs = twc.Variable(default=None)
    _uuid = twc.Param(default=None)
    widget = twc.Variable(default=None)
    active_tab = twc.Variable(default=None)
    tabs = twc.Variable(default=None)

    default_tab = None

    def __init__(self, *args, **kw):
        super(TabWidget, self).__init__(*args, **kw)
        self._uuid = str(uuid.uuid4())
        self._expanded_tabs = collections.OrderedDict()
        for key, widget_key in self.tabs.items():
            display_name = key
            key = key.lower()
            self._expanded_tabs[key] =  {'display_name': display_name,
                                         'widget_key': widget_key}

    def prepare(self):
        super(TabWidget, self).prepare()
        if not self.args:
            self.args = []
        if not self.kwds:
            self.kwds = {}

        if isinstance(self.args, mako.runtime.Undefined):
            self.args = []
        if isinstance(self.kwds, mako.runtime.Undefined):
            self.kwds = {}

        if len(self.args) > 0:
            active_tab = self.args.pop(0).lower()
        else:
            active_tab = self.default_tab.lower()

        self.widget = moksha.utils.get_widget(self._expanded_tabs[active_tab]['widget_key'])
        self.tabs = self._expanded_tabs
        self.active_tab = active_tab

        if isinstance(self.base_url, Template):
            self.base_url = self.base_url.render(**self.__dict__)


class PackageNavWidget(TabWidget):
    tabs = collections.OrderedDict([('Overview', 'package.overview'),
                                    ('Bugs', 'package.bugs')])
    base_url = Template(text='/${kwds["package_name"]}/');
    default_tab = 'Overview'
    args = twc.Param(default=None)
    kwds = twc.Param(default=None)


class PackageWidget(twc.Widget):
    template = "mako:fedoracommunity/widgets/package/templates/package_chrome.mak"

    package_name = twc.Param()
    args = twc.Param(default=None)
    kwds = twc.Param(default=None)
    latest_build = twc.Variable()
    navigation_widget = PackageNavWidget

    def prepare(self):
        super(PackageWidget, self).prepare()
        name = self.args.pop(0)
        self.kwds['package_name'] = name
        xapian_conn = get_connector('xapian')
        result = xapian_conn.get_package_info(name)
        self.package_info = result
        koji = get_connector('koji')
        try:
            builds = koji._koji_client.getLatestBuilds('dist-rawhide', package=name)
            if builds:
                self.latest_build = builds[0]['version'] + '-' + \
                                    builds[0]['release']
            else:
                self.latest_build = 'Not built in rawhide'
        except Exception, e:
            log.error('Unable to query koji: %s' % str(e))
            self.latest_build = 'Koji unavailable'
