from moksha.lib.base import BaseController
from moksha.lib.helpers import Category, MokshaApp, Not, not_anonymous, MokshaWidget
from moksha.api.widgets.containers import DashboardContainer
from moksha.api.widgets import ContextAwareWidget
from tg import expose, tmpl_context

class OverviewContainer(DashboardContainer, ContextAwareWidget):
    template = 'mako:fedoracommunity.mokshaapps.overviewresource.templates.overviewcontainer'
    layout = [Category('left-content-column',
                       [MokshaApp('Latest Rawhide Builds', 'fedoracommunity.builds/table'),
                        MokshaApp('Latest Stable Updates','fedoracommunity.updates/table',
                                  params={"filters":'{"status":"stable"}', "uid":"stable"}),
                        MokshaApp('Latest Testing Updates','fedoracommunity.updates/table',
                                  params={"filters":'{"status":"testing"}', "uid":"testing"}),
                        MokshaApp('Planet Fedora','fedoracommunity.planetfedora')
                        ]),
              Category('right-content-column',
                       [MokshaWidget(None, 'fedoracommunity.login', auth=Not(not_anonymous())),
                        MokshaApp('Alerts', 'fedoracommunity.alerts'),
                        MokshaApp('Quick Links', 'fedoracommunity.quicklinks', auth=not_anonymous()),
                        MokshaApp('Quick Links', 'fedoracommunity.mypackages', auth=not_anonymous())
                       ]
                      )
              ]

overview_container = OverviewContainer('overview')

class RootController(BaseController):

    @expose('mako:fedoracommunity.mokshaapps.overviewresource.templates.index')
    def index(self):
        tmpl_context.widget = overview_container

        return dict()
