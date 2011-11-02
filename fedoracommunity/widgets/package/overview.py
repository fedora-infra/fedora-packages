import tw2.core as twc
import collections

from package import TabWidget
from updates import ActiveReleasesGrid

from mako.template import Template

from moksha.api.connectors import get_connector

class OverviewNavWidget(TabWidget):
    tabs = collections.OrderedDict([('Details', 'package.overview.details'),
                                    ('Builds', 'package.overview.builds'),
                                    ('Updates', 'package.overview.updates')])
    base_url = Template('/${kwds["package_name"]}/overview/')
    default_tab = 'Details'


class OverviewWidget(twc.Widget):
    template = 'mako:fedoracommunity/widgets/package/templates/overview.mak'
    args = twc.Param()
    kwds = twc.Param()
    nav_widget = OverviewNavWidget


class Details(twc.Widget):
    template = 'mako:fedoracommunity/widgets/package/templates/details.mak'
    kwds = twc.Param('Data passed in from the tabs')
    package_info = twc.Param('A dict containing package details from xapian')
    active_releases_widget = ActiveReleasesGrid

    def prepare(self):
        super(Details, self).prepare()
        package_name = self.kwds['package_name']
        xapian_conn = get_connector('xapian')
        result = xapian_conn.get_package_info(package_name)
        self.package_info = result


class Builds(twc.Widget):
    template = 'mako:fedoracommunity/widgets/package/templates/builds.mak'

class Updates(twc.Widget):
    template = 'mako:fedoracommunity/widgets/package/templates/updates.mak'
