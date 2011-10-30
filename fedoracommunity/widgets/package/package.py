from tw.api import Widget
import collections
import mako
import uuid

import moksha

from fedoracommunity.connectors.xapianconnector import XapianConnector

class BugsWidget(Widget):
    template = u"""Bugs
    dude
    """
    engine_name = 'mako'

class TabWidget(Widget):
    template="mako:fedoracommunity.widgets.package.templates.tabs"
    params = ['base_url', 'args', 'kwds']
    tabs = None
    default_tab = None
    base_url = '/'
    args = []
    kwds = {}

    def __init__(self):
        self._uuid = uuid.uuid4()
        self._expanded_tabs = collections.OrderedDict()
        for key, widget_key in self.tabs.items():
            display_name = key
            key = key.lower()
            self._expanded_tabs[key] =  {'display_name': display_name,
                                         'widget_key': widget_key}
        Widget.__init__(self)

    def update_params(self, d):
        args = d.get('args', [])
        kwds = d.get('kwds', {})

        if isinstance(args, mako.runtime.Undefined):
            args = []
        if isinstance(kwds, mako.runtime.Undefined):
            kwds = {}


        if len(args) > 0:
            active_tab = args.pop(0).lower()
        else:
            active_tab = self.default_tab.lower()

        d['widget'] = moksha.get_widget(self._expanded_tabs[active_tab]['widget_key'])
        d['tabs'] = self._expanded_tabs
        d['args'] = args
        d['kwds'] = kwds
        d['_uuid'] = self._uuid
        d['base_url'] = self.base_url

        super(TabWidget, self).update_params(d)

class PackageNavWidget(TabWidget):
    tabs = collections.OrderedDict([('Overview', 'package.overview'),
                                    ('Bugs', 'package.bugs')])
    base_url = '/*/';
    default_tab = 'Overview'

package_nav_widget = PackageNavWidget()

class PackageWidget(Widget):
    template = "mako:fedoracommunity/widgets/package/templates/package_chrome.mak"
    params = ['package_name', 'args', 'kwds']
    package_name = None
    args = []
    kwds = {}

    def update_params(self, d):
        d['widget'] = package_nav_widget
        args = d.get('args')
        name = args.pop(0)
        d['kwds']['package_name'] = name

        xapian_conn = XapianConnector(None, None)
        result = xapian_conn.get_package_info(name)
        d['package_info'] = result

        super(PackageWidget, self).update_params(d)
