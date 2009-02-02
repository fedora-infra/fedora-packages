import paste
import webob
import time
import logging
from fedora.client import ProxyClient, FedoraServiceError, AuthError
import urllib2
import tg
import uuid

from repoze.who.middleware import PluggableAuthenticationMiddleware

from repoze.who.interfaces import IIdentifier
from repoze.who.interfaces import IChallenger
from repoze.who.plugins.form import RedirectingFormPlugin
from repoze.who.classifiers import default_request_classifier
from repoze.who.classifiers import default_challenge_decider

from repoze.what.adapters import BaseSourceAdapter

from beaker.cache import Cache

from repoze.who.interfaces import IChallenger, IIdentifier

from Cookie import SimpleCookie

import beaker   

import pkg_resources

import os
import sys
import logging
import pylons

log = logging.getLogger(__name__)

FAS_CACHE_TIMEOUT=20 #in seconds

fasurl = tg.config.get('fedoracommunity.fas.baseurl')
fas_cache = Cache('fas_repozewho_cache')

def fas_make_who_middleware(app, log_stream):
    faswho = FASWhoPlugin(fasurl)
    
    form = RedirectingFormPlugin('/login', '/login_handler', '/logout', rememberer_name='fasident')
    form.classifications = { IIdentifier:['browser'],
                             IChallenger:['browser'] } # only for browser
    identifiers = [('form', form),('fasident', faswho)]
    authenticators = [('fasauth', faswho)]
    challengers = [('form',form)]
    mdproviders = [('fasmd', faswho)]
    
    if os.environ.get('FAS_WHO_LOG'):
        log_stream = sys.stdout
    
    middleware = PluggableAuthenticationMiddleware(
        app,
        identifiers,
        authenticators,
        challengers,
        mdproviders,
        default_request_classifier,
        default_challenge_decider,
        log_stream = log_stream
        )
    
    return middleware


class FasClient(ProxyClient):
    visit_name = 'tg-visit'
    
    def __init__(self, baseURL):
        super(FasClient, self).__init__(baseURL, session_as_cookie=False)

    def convert_cookie(self, cookie):
        sc = SimpleCookie()
        for key, value in cookie.iteritems():
            sc[key] = value
            
        return sc
    
    def login(self, login, password):
        return self.send_request("login", 
                                 auth_params={'username': login, 
                                              'password':password})
        
    def logout(self, session_id):
        auth_params = {'session_id': session_id}
            
        return self.send_request("logout", auth_params = auth_params)

    def keep_alive(self, session_id, get_user_info):
        if not session_id:
            return None

        method = ''
        if get_user_info:
            method = 'user/view'
            
        auth_params = {'session_id': session_id}
        
        result = None
        try:
            result = self.send_request(method, auth_params = auth_params)
        except AuthError, e:
            log.warning(e)

        return result

class FASWhoPlugin(object):    
    def __init__(self, url):
        self.url = url
        self._session_cache = {}
        self._metadata_plugins = []
        
        for entry in pkg_resources.iter_entry_points('fas.repoze.who.metadata_plugins'):
            self._metadata_plugins.append(entry.load())
        
        
    def keep_alive(self, session_id):
        log.info("Keep alive cache miss")
        fas = FasClient(self.url)
        
        linfo = fas.keep_alive(session_id, True)
        
        return linfo
    
    def identify(self, environ):
        req = webob.Request(environ)
        
        log.info('Identify')
        errk = req.cookies.get('fas_error_key')
        if errk:
            log.info('''There was an error set in the last session - 
                        retrieving error message''')
            try:
                err = fas_cache.get_value(key=errk)
                fas_cache.remove_value(errk)
                environ['FAS_AUTH_ERROR'] = err
                return None
            except:
                pass
        
        cookie = req.cookies.get('tg-visit')
 
        if cookie is None:
            return None
        
        log.info("Request identify for cookie " + cookie)
        linfo = fas_cache.get_value(key=cookie + "_identity",
                                    createfunc=lambda: self.keep_alive(cookie),
                                    type="memory",
                                    expiretime=FAS_CACHE_TIMEOUT)

        if not linfo:
            self.forget(environ, None)
            return None
                    
        if not isinstance(linfo, tuple):
            return None
        
        try:
            me = linfo[1]
            me.update({'repoze.who.userid':me['person']['username']})
            environ['FAS_LOGIN_INFO'] = linfo
            return linfo[1]
        except Exception, e:
            log.warning(e)
            return None
        
    def remember(self, environ, identity):
        log.info('Remeber')
        err = identity.get('error')
        if err:
            log.info('''There was an error set in this session -
                        saving error message for next page redirect''')
            cache_error_key=str(uuid.uuid4()) + '_fas_error'
            set_cookie = 'fas_error_key="%s"; Path=/;' % (cache_error_key)
            fas_cache.set_value(cache_error_key, err, type="memory",
                                                      expiretime=120)
            return [('Set-Cookie', set_cookie)]
        
        result = []
        req = webob.Request(environ)
        if req.cookies.get('fas_error_key'):
            expired = ('fas_error_key=""; Path=/; Expires=Sun, 10-May-1971 11:59:00 GMT')
            result.append(('Set-Cookie', expired))
        
        linfo = environ.get('FAS_LOGIN_INFO')
        if isinstance(linfo, tuple):
            session_id = linfo[0]
            set_cookie = 'tg-visit=%s; Path=/;' % (session_id)
            result.append(('Set-Cookie', set_cookie))
            return result
        return None

    def forget(self, environ, identity):
        log.info("Forget")
        # return a expires Set-Cookie header
        req = webob.Request(environ)
        
        linfo = environ.get('FAS_LOGIN_INFO')
        if isinstance(linfo, tuple):
            session_id = linfo[0]
            log.info("Forgetting login data for cookie %s" % (session_id))
            
            fas = FasClient(self.url)
            fas.logout(session_id)
            
            result = []
            fas_cache.remove_value(key=session_id + "_identity")
            expired = ('tg-visit=""; Path=/; Expires=Sun, 10-May-1971 11:59:00 GMT')
            result.append(('Set-Cookie', expired))
            environ['FAS_LOGIN_INFO'] = None
            return result
        
        return None
     
    # IAuthenticatorPlugin
    def authenticate(self, environ, identity):
        log.info('Authenticate')
        try:
            login = identity['login']
            password = identity['password']
        except KeyError:
            return None

        user_data = ""
        try:
            fas = FasClient(self.url)
            user_data = fas.login(login, password)
        except AuthError, e:
            log.info('Authentication failed, setting error')
            err = 'ERROR: Could not log in. Invalid username or password.'
            environ['FAS_AUTH_ERROR'] = err
            identity['error'] = err
            
            return 'error'
            
        if user_data:
            if isinstance(user_data, tuple):
                environ['FAS_LOGIN_INFO']=fas.keep_alive(user_data[0], True)
                return login
    
        return None
    
    def get_metadata(self, environ):
        log.info("Metadata cache miss - refreshing metadata")
        info = environ.get('FAS_LOGIN_INFO')
        identity = {}
        
        if info is not None:
            identity.update(info[1])
            
        for plugin in self._metadata_plugins:
            plugin(identity)
        
        # we don't define permissions since we don't
        # have any peruser data though other services
        # may wish to add another metadata plugin to do so
        
        if not identity.has_key('permissions'):
            identity['permissions'] = set();

        # we keep the approved_memberships list because there is also an
        # unapproved_membership field.  The groups field is for repoze.who
        # group checking and may include other types of groups besides 
        # memberships in the future (such as special fedora community groups)
        
        groups = set()
        for g in identity['person']['approved_memberships']:
            groups.add(g['name'])
            
        identity['groups'] = groups   
        return identity
        
    def add_metadata(self, environ, identity):
        log.info('Metadata')
        req = webob.Request(environ)
        
        if identity.get('error'):
            log.info('Error exists in session, no need to set metadata') 
            return 'error'
             
        cookie = req.cookies.get('tg-visit')

        if cookie is None:
            return None
        
        log.info('Request metadata for cookie %s' % (cookie))        
        info = fas_cache.get_value(key=cookie + '_metadata',
                                   createfunc=lambda: self.get_metadata(environ),
                                   type="memory",
                                   expiretime=FAS_CACHE_TIMEOUT)
   
           
        identity.update(info)

    def __repr__(self):
        return '<%s %s>' % (self.__class__.__name__, id(self))


"""
We don't need any of this, we simply need to set identity['groups']
and identity['permissions'] in our who metadata layer I'm leaving
this skeleton here just incase we do want to implement getting the 
whole FAS database (we don't though)


class FASWhatGroupAdaptor(BaseSourceAdaptor):
    def __init__(self):
        super(FASWhatGroupAdaptor, self).__init__(writable=False)

    def _get_all_sections(self):
        return {}
    
    def _get_section_items(self, section):
        return set([])
    
    # hint is the repoze.who.ident hash
    def _find_sections(self, hint):
        return ()
    
    def _section_exists(self, section):
        return True

class FASWhatPermAdaptor(BaseSourceAdaptor):
    # we don't handle permissions yet
    def __init__(self):
        super(FASWhatGroupAdaptor, self).__init__(writable=False)

    def _get_all_sections(self):
        return {}
    
    def _get_section_items(self, section):
        return set([])
    
    # hint is the repoze.who.ident hash
    def _find_sections(self, hint):
        return ()
    
    def _section_exists(self, section):
        return False

"""