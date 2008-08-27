import paste
import webob
import time
import logging
from fedora.client import ProxyClient, FedoraServiceError, AuthError
import urllib2

from repoze.who.interfaces import IIdentifier
from repoze.who.interfaces import IChallenger
from repoze.who.plugins.form import RedirectingFormPlugin
from repoze.who.classifiers import default_request_classifier
from repoze.who.classifiers import default_challenge_decider
from repoze.who.middleware import PluggableAuthenticationMiddleware

from repoze.who.interfaces import IChallenger, IIdentifier

from Cookie import SimpleCookie

import pkg_resources

import os
import sys

FAS_CACHE_TIMEOUT=5

fasurl = 'https://admin.fedoraproject.org/accounts'

def fas_make_who_middleware(app, config):
    faswho = FASWhoPlugin(fasurl)
    
    form = RedirectingFormPlugin('/login', '/login_handler', '/logout', rememberer_name='fasident')
    form.classifications = { IIdentifier:['browser'],
                             IChallenger:['browser'] } # only for browser
    identifiers = [('form', form),('fasident', faswho)]
    authenticators = [('fasauth', faswho)]
    challengers = [('form',form)]
    mdproviders = [('fasmd', faswho)]
    
    log_stream = None
    if os.environ.get('WHO_LOG'):
        log_stream = sys.stdout
    
    middleware = PluggableAuthenticationMiddleware(
        app,
        identifiers,
        authenticators,
        challengers,
        mdproviders,
        default_request_classifier,
        default_challenge_decider,
        log_stream = log_stream,
        log_level = logging.DEBUG
        )
    
    return middleware


class FasClient(ProxyClient):
    visit_name = 'tg-visit'
    
    def __init__(self, baseURL):
        super(FasClient, self).__init__(baseURL)

    def convert_cookie(self, cookie):
        sc = SimpleCookie()
        for key, value in cookie.iteritems():
            sc[key] = value
            
        return sc
    
    def login(self, login, password):
        return self.send_request("login", 
                                 auth_params={'username': login, 
                                              'password':password})
        
    def logout(self, cookie):
        if cookie and not isinstance(cookie, SimpleCookie):
            cookie = self.convert_cookie(cookie)
            
        auth_params = {'cookie': cookie}
            
        return self.send_request("logout", auth_params = auth_params)

    def keep_alive(self, cookie, get_user_info):
        if cookie:
            if not cookie.get('tg-visit', None):
                return None
            
            if not isinstance(cookie, SimpleCookie):
                cookie = self.convert_cookie(cookie)
        
        method = ''
        if get_user_info:
            method = 'user/view'
            
        auth_params = {'cookie': cookie}
        
        result = None
        try:
            result = self.send_request(method, auth_params = auth_params)
        except AuthError, e:
            
            print e

        return result

class FASWhoPlugin(object):    
    def __init__(self, url):
        self.url = url
        self._session_cache = {}
        self._metadata_plugins = []
        
        for entry in pkg_resources.iter_entry_points('fas.repoze.who.metadata_plugins'):
            self._metadata_plugins.append(entry.load())
        
    def identify(self, environ):
        req = webob.Request(environ)
                    
        cookie = req.cookies.get('tg-visit')

        if cookie is None:
            return None
        else:
            fas = FasClient(self.url)
            
            linfo = fas.keep_alive(req.cookies, True)
            if not linfo:
                self.forget(environ, None)
                return None
                    
        if not isinstance(linfo, tuple):
            return None
        else:
            try:
                me = linfo[1]
                me.update({'repoze.who.userid':me['person']['username']})
                environ['FAS_LOGIN_INFO'] = linfo
                return linfo[1]
            except Exception, e:
                print e, linfo
                return None
        
    def remember(self, environ, identity):
        linfo = environ.get('FAS_LOGIN_INFO')
        if isinstance(linfo, tuple):
            cookies = linfo[0]
            result = []
            for name, value in cookies.iteritems():
                # return a Set-Cookie header
                set_cookie = '%s=%s; Path=/;' % (name, value)
                result.append(('Set-Cookie', set_cookie))
            return result
        return None

    def forget(self, environ, identity):
        # return a expires Set-Cookie header
        req = webob.Request(environ)
                    
        req.cookies['tg-visit'] = None
        
        linfo = environ.get('FAS_LOGIN_INFO')
        if isinstance(linfo, tuple):
            cookies = linfo[0]
            result = []
            for name in cookies.iterkeys():
                expired = ('%s=""; Path=/; Expires=Sun, 10-May-1971 11:59:00 GMT' %
                           name)
                result.append(('Set-Cookie', expired))
                environ['FAS_LOGIN_INFO'] = None
                
                cookies['tg-visit'] = None
            return result
        return None
    
    # IAuthenticatorPlugin
    def authenticate(self, environ, identity):
        try:
            login = identity['login']
            password = identity['password']
        except KeyError:
            return None

        fas = FasClient(self.url)
        user_data = fas.login(login, password)
        if user_data:
            if isinstance(user_data, tuple) and isinstance(user_data[0], SimpleCookie):
                environ['FAS_LOGIN_INFO']=fas.keep_alive(user_data[0], True)
                return login
    
        return None
    
    def add_metadata(self, environ, identity):
        info = environ.get('FAS_LOGIN_INFO')

        if info is not None:
            identity.update(info[1])
            
        for plugin in self._metadata_plugins:
            plugin(identity)

    def __repr__(self):
        return '<%s %s>' % (self.__class__.__name__, id(self))

