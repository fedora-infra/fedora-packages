import logging
import tw2.core as twc

from fedoracommunity.connectors.api import get_connector
from fedoracommunity.widgets.grid import Grid

log = logging.getLogger(__name__)

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
        package_name = self.kwds['package_name']
        xapian_conn = get_connector('xapian')
        result = xapian_conn.get_package_info(package_name)
        self.package_name = package_name
        self.package_info = result
        latest_build = twc.Variable(default='Koji unavailable')
        super(Details, self).prepare()

        if result['name'] == package_name:
            self.summary = result['summary']
            self.description = result['description']
        else:
            for subpkg in result['sub_pkgs']:
                if subpkg['name'] == package_name:
                    self.summary = subpkg['summary']
                    self.description = subpkg['description']
                    break

        self.package_info = result

        koji = get_connector('koji')
        try:
            builds = koji._koji_client.getLatestBuilds('rawhide', package=result['name'])
            if builds:
                self.latest_build = builds[0]['version'] + '-' + \
                                    builds[0]['release']
            else:
                self.latest_build = 'Not built in rawhide'
        except Exception, e:
            log.error('Unable to query koji: %s' % str(e))

    def __repr__(self):
        return "<Details %s>" % self.kwds
