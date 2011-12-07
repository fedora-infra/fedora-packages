import tw2.core as twc
import collections

from package import TabWidget
from mako.template import Template
from moksha.api.connectors import get_connector
from moksha.api.widgets import Grid

class OverviewNavWidget(TabWidget):
    tabs = collections.OrderedDict([('Details', 'package.overview.details'),
                                    ('Builds', 'package.overview.builds'),
                                    ('Updates', 'package.overview.updates')])
    base_url = Template(text='/${kwds["package_name"]}/overview/')
    default_tab = 'Details'


class OverviewWidget(twc.Widget):
    template = 'mako:fedoracommunity.widgets.package.templates.overview'
    args = twc.Param()
    kwds = twc.Param()
    nav_widget = OverviewNavWidget


class ActiveReleasesGrid(Grid):
    template = 'mako:fedoracommunity.widgets.package.templates.active_releases'
    package_name = twc.Param('The name of the package to view')
    resource = 'bodhi'
    resource_path = 'query_active_releases'

    def prepare(self):
        self.filters = {'package': self.package_name}
        self.rows_per_page = 10

        # Must do this last for our Grids
        super(ActiveReleasesGrid, self).prepare()


class Details(twc.Widget):
    template = 'mako:fedoracommunity.widgets.package.templates.details'
    kwds = twc.Param('Data passed in from the tabs')
    package_info = twc.Param('A dict containing package details from xapian')
    active_releases_widget = ActiveReleasesGrid

    def prepare(self):
        super(Details, self).prepare()
        package_name = self.kwds['package_name']
        xapian_conn = get_connector('xapian')
        result = xapian_conn.get_package_info(package_name)

        if result['name'] == package_name:
            self.summary = result['summary']
            self.description = result['description']
        else:
            for subpkg in result['sub_pkgs']:
                if subpkg['name'] == package_name:
                    self.summary = subpkg['summary']
                    self.description = subpkg['description']
                    break;

        self.package_info = result
