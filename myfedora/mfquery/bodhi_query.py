import simplejson, urllib, urllib2, cookielib 

from turbogears import controllers, expose, identity, config

from myfedora.urlhandler import BodhiURLHandler

def get_info(kwarg_compat, **kw):
    kw.update({
       'tg_format': 'json'
    })

    if not kw.get('package', None):
        return {}

    url = BodhiURLHandler().get_base_url() + 'list?' 
    url += urllib.urlencode(kw)

    cj = cookielib.CookieJar()

    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    request = urllib2.Request(url)
    cookieName = config.get('visit.cookie.name', 'tg-visit')
    request.add_header("Cookie", cookieName + "=" + identity.current.visit_key)
    response = opener.open(request)

    json_data = simplejson.load(response)
    if kwarg_compat:
        # when using dicts as kwargs (e.g. **{}) the top level keys can not
        # be unicode in Python 2.5 and below but simplejson returns all keys
        # as unicode
        compat_dict = {}
        for key, value in json_data.iteritems():
            compat_dict[str(key)] = value
            
        json_data = compat_dict

    return json_data


class BodhiQuery(controllers.Controller):
    @expose("json", allow_json=True)
    def get_info(self, *args, **kw): 
        return get_info(False, **kw)

