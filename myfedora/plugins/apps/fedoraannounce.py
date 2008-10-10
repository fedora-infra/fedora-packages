from tg import url
from tw.api import Widget, JSLink
from tw.jquery import jquery_js, jQuery
from myfedora.lib.app_factory import AppFactory
import feedparser
import re

ui_js = JSLink(link='/javascript/myfedora.ui.js')

src_re = re.compile('src\s*=\s*"([^"]*)"')

class FedoraAnnounceBaseWidget(Widget):
    """ The base widget for the fedora announce.
    """
    params = []
    javascript=[jquery_js, ui_js]
    
    url = 'https://www.redhat.com/archives/fedora-announce-list/'
    rssurl = 'http://localhost:8080/misc/fedora_announce.xml'
    
    def update_params(self, d):
        super(FedoraAnnounceBaseWidget, self).update_params(d)
        
        entry_list = []
        
        d['url'] = self.url
        rssfeed = feedparser.parse(self.rssurl)
        show = d.get('show', None)

        if show:
            try:
                show = int(show)
            except:
                pass

        for c, entry in enumerate(rssfeed.entries):
            if show and (c >= show):
                break
            
            entry['uid'] = d['config']['uid'] + '_' + str(c)
                    
            entry_list.append(entry)
            
            

        d.update({'entries': entry_list})

    def __str__(self):
        return "<%s %s>" % (self.__class__.__name__, self.id)

class FedoraAnnounceHomeWidget(FedoraAnnounceBaseWidget):
    template = 'genshi:myfedora.plugins.apps.templates.fedoraannouncehome'

class FedoraAnnounceCanvasWidget(FedoraAnnounceBaseWidget):
    template = 'genshi:myfedora.plugins.apps.templates.fedoraannouncecanvas'

class FedoraAnnounceApp(AppFactory):
    entry_name = 'fedoraannounce'

    def __init__(self, app_config_id, 
                 width=None, 
                 height=None, 
                 view='Home',
                 show = None,
                 charcount=500,
                 **kw):
        super(FedoraAnnounceApp, self).__init__(app_config_id, 
                                              width, 
                                              height, 
                                              view,
                                              show = show,
                                              charcount = charcount,
                                              **kw)

        
