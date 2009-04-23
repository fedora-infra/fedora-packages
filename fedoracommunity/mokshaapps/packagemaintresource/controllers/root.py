from moksha.lib.base import Controller
from moksha.lib.helpers import MokshaApp
from tg import expose, tmpl_context
from fedoracommunity.widgets import SubTabbedContainer

class AllPackagesTabbedNav(SubTabbedContainer):
    tabs= (MokshaApp('Packages', 'fedoracommunity.packages'),
           MokshaApp('Builds', 'fedoracommunity.builds'),
           MokshaApp('Updates', 'fedoracommunity.updates'),
          )

class SelectedPackageTabbedNav(SubTabbedContainer):
    tabs= (MokshaApp('Overview', 'fedoracommunity.packages',
                     content_id = 'package_overview',
                     params={'package':''}),
           MokshaApp('Package Details', 'fedoracommunity.packages/details',
                     content_id = 'details',
                     params={'package':''}),
           MokshaApp('Package Maintenance Tools', 'fedoracommunity.packages/tools',
                     content_id = 'tools',
                     params={'package':''}),
          )

all_packages_nav = AllPackagesTabbedNav('packagemaintnav')
selected_package_nav = SelectedPackageTabbedNav('selectedpackagenav')

class RootController(Controller):

    @expose('mako:moksha.templates.widget')
    def index(self, **kwds):
        options = {}
        package = kwds.get('package')
        tmpl_context.widget = all_packages_nav
        if package:
            options['package'] = package
            tmpl_context.widget = selected_package_nav

        return {'options': options}
