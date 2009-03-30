from moksha.api.widgets.containers import DashboardContainer
from moksha.api.widgets import ContextAwareWidget
from moksha.api.connectors import get_connector

class PackagesDashboardContainer(DashboardContainer, ContextAwareWidget):
    template = 'mako:fedoracommunity.mokshaapps.packages.templates.single_col_dashboard'

    def update_params(self, d):
        super(PackagesDashboardContainer, self).update_params(d)

        # get the package description
        p = d.get('package')
        conn = get_connector('pkgdb')
        info = conn.get_basic_package_info(p)
        d['pkg_description'] = info['description']
        d['pkg_summary'] = info['summary']
