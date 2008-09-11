from tg import url
from tw.api import Widget, JSLink
from tw.jquery import jquery_js, jQuery
from myfedora.lib.app_factory import AppFactory
import feedparser

ui_js = JSLink(link='/javascript/myfedora.ui.js')

class PlanetFedoraBaseWidget(Widget):
    """ The base widget for the Fedora People view.
    """
    params = []
    javascript=[jquery_js, ui_js]
    
    atomurl = 'http://planet.fedoraproject.org/atom.xml'
    rssurl = 'http://planet.fedoraproject.org/rss20.xml'
    
    def update_params(self, d):
        super(PlanetFedoraBaseWidget, self).update_params(d)
        
        view_users_list = d['view_users_list']
        entry_list = []
        
        atomfeed = feedparser.parse(self.atomurl)
        show = d.get('show', None)

        for c, atomentry in enumerate(atomfeed.entries):
            if not view_users_list or entry.author.name in view_users_list:
                atomentry['uid'] = d['config']['uid'] + '_' + str(c)
                atomentry.author_detail['hackergotchi'] = 'http://planet.fedoraproject.org/images/heads/default.png'
                entry_list.append(atomentry)
                if show and c >= show:
                    break

        d.update({'entries': entry_list})

    def __str__(self):
        return "<%s %s>" % (self.__class__.__name__, self.id)

class PlanetFedoraHomeWidget(PlanetFedoraBaseWidget):
    template = 'genshi:myfedora.plugins.apps.templates.planetfedorahome'

class PlanetFedoraCanvasWidget(PlanetFedoraBaseWidget):
    template = 'genshi:myfedora.plugins.apps.templates.planetfedoracanvas'

class PlanetFedoraApp(AppFactory):
    entry_name = 'planetfedora'

    def __init__(self, app_config_id, 
                 width=None, 
                 height=None, 
                 view='Home', 
                 view_users_list = None,
                 show = None,
                 **kw):
        super(PlanetFedoraApp, self).__init__(app_config_id, 
                                              width, 
                                              height, 
                                              view,
                                              view_users_list = view_users_list,
                                              show = show,
                                              **kw)

        
