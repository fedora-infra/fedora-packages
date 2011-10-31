from tw.api import Widget
import collections
import mako

from package import TabWidget
from updates import active_releases_widget

from mako.template import Template

from moksha.api.connectors import get_connector

class OverviewNavWidget(TabWidget):
    tabs = collections.OrderedDict([('Details', 'package.overview.details'),
                                    ('Builds', 'package.overview.builds'),
                                    ('Updates', 'package.overview.updates')])
    base_url = Template('/${kwds["package_name"]}/overview/')
    default_tab = 'Details'

overview_nav_widget = OverviewNavWidget()

class OverviewWidget(Widget):
    template = 'mako:fedoracommunity/widgets/package/templates/overview.mak'

    def update_params(self, d):
        super(OverviewWidget, self).update_params(d)
        d['nav_widget'] = overview_nav_widget
        args = d.get('args', [])
        if len(args) > 0:
            overview_component = args.pop(0)

class Details(Widget):
    template = 'mako:fedoracommunity/widgets/package/templates/details.mak'
    def update_params(self, d):
        super(Details, self).update_params(d)
        package_name = d['kwds']['package_name']

        xapian_conn = get_connector('xapian')
        result = xapian_conn.get_package_info(package_name)
        d['package_info'] = result
        d['active_releases_widget'] = active_releases_widget;

class Builds(Widget):
    template = u"""Builds
    dude
    """
    engine_name = 'mako'

class Updates(Widget):
    template = u"""Updates
    dude
    """
    engine_name = 'mako'
    
details_widget = Details()
builds_widget = Builds()
updates_widget = Updates()
