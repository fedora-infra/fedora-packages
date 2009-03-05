from moksha.lib.base import Controller
from moksha.lib.helpers import Category, MokshaApp, Not, not_anonymous, MokshaWidget
from moksha.api.widgets.containers import DashboardContainer
from moksha.api.widgets import ContextAwareWidget
from tg import expose, tmpl_context

class OverviewContainer(DashboardContainer, ContextAwareWidget):
    template = 'mako:fedoracommunity.mokshaapps.overviewresource.templates.overviewcontainer'
    layout = [Category('left-content-column',
                       [MokshaApp('Latest Rawhide Builds', 'fedoracommunity.builds/table',
                                  params={"rows_per_page": 5}),
                        MokshaApp('Latest Stable Updates','fedoracommunity.updates/table',
                                  params={"filters":'{"status":"stable"}', "rows_per_page": 5, "uid":"stable"}),
                        MokshaApp('Latest Testing Updates','fedoracommunity.updates/table',
                                  params={"filters":'{"status":"testing"}', "rows_per_page": 5, "uid":"testing"}),
                        MokshaWidget('Planet Fedora','fedoracommunity.planet', params={'id': 'planet'}),
                        ]),
              Category('right-content-column',
                       [MokshaWidget(None, 'fedoracommunity.login',
                                     params={'came_from': '/'},
                                     css_class='',
                                     auth=Not(not_anonymous())),
                        MokshaApp('Alerts', 'fedoracommunity.alerts'),
                        MokshaApp('Quick Links', 'fedoracommunity.quicklinks', auth=not_anonymous()),
                        MokshaApp('My Packages', 'fedoracommunity.packages/mypackages', auth=not_anonymous())
                       ],
                       default_child_css="panel"
                      )
              ]

overview_container = OverviewContainer('overview')

class RootController(Controller):

    @expose('mako:fedoracommunity.mokshaapps.overviewresource.templates.index')
    def index(self):
        tmpl_context.widget = overview_container
        return dict()
