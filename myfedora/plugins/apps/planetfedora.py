from tg import url
from tw.api import Widget, JSLink, CSSLink
from tw.jquery import jquery_js, jQuery
from myfedora.lib.app_factory import AppFactory
from myfedora.lib.utils import HRElapsedTime
import feedparser
import re

from pylons import cache

ui_js = JSLink(link='/javascript/myfedora.ui.js')
planet_css = CSSLink(link='/css/planet-fedora-bubbles.css')

src_re = re.compile('src\s*=\s*"([^"]*)"')

class PlanetFedoraBaseWidget(Widget):
    """ The base widget for the Fedora People view.
    """
    params = []
    javascript=[jquery_js, ui_js]
    css=[planet_css]
    
    atomurl = 'http://planet.fedoraproject.org/atom.xml'
    rssurl = 'http://planet.fedoraproject.org/rss20.xml'
    
    def get_atom_entries(self):
        atomfeed = feedparser.parse(self.atomurl)
        return atomfeed
        
    def update_params(self, d):
        super(PlanetFedoraBaseWidget, self).update_params(d)
        
        view_users_list = d['view_users_list']
        entry_list = []

        c = cache.get_cache('myfedora')        
        atomfeed = c.get_value(key='planetfedora',
                               createfunc=self.get_atom_entries,
                               type="memory",
                               expiretime=60)
        
        show = d.get('show', None)

        for c, atomentry in enumerate(atomfeed.entries):
            if not view_users_list or entry.author.name in view_users_list:
                atomentry['uid'] = d['config']['uid'] + '_' + str(c)
                
                value = atomentry.content[0].value.lstrip()
                if value.startswith('<img'):
                    pos = value.find('/>') + 2
                
                    img_tag = value[0:pos]
                    atomentry.content[0].value=value[pos:]
                    
                    m = src_re.search(img_tag)
                    atomentry.author_detail['hackergotchi'] = 'http://planet.fedoraproject.org/images/heads/default.png'
                    
                    try:
                        atomentry.author_detail['hackergotchi'] = m.group(1)
                    except Exception, e:
                        print e
            
                # make time look nice
                hret = HRElapsedTime()
                hret.set_parse_format('%Y-%m-%dT%H:%M:%S+00:00')
                hret.set_output_format('%H:%M UTC')
                hret.long_date = False
                hret.set_start_timestr(atomentry.updated)
                hret.set_end_time_to_now()
                
                atomentry['elapsed_time'] = hret.get_hr_elapsed_time()
                atomentry['time'] = hret.get_hr_start_time()
                
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

        
