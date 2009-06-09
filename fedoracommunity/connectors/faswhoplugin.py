# This file is part of Fedora Community.
# Copyright (C) 2008-2009  Red Hat, Inc.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import tg
import sys
import webob
import logging
import pkg_resources

from beaker.cache import Cache
from fedora.client import ProxyClient, AuthError
from paste.httpexceptions import HTTPUnauthorized, HTTPFound
from repoze.who.middleware import PluggableAuthenticationMiddleware
from repoze.who.plugins.form import RedirectingFormPlugin
from repoze.who.classifiers import default_request_classifier
from repoze.who.classifiers import default_challenge_decider
from repoze.who.interfaces import IChallenger, IIdentifier
from Cookie import SimpleCookie
from paste.request import parse_dict_querystring, parse_formvars
from urllib import quote_plus

from moksha.middleware.csrf import CSRFMetadataProvider
from moksha.api.errorcodes import login_err
from moksha.lib.helpers import replace_app_header

log = logging.getLogger(__name__)

#FAS_CACHE_TIMEOUT=20 #in seconds
FAS_CACHE_TIMEOUT=900 # 15 minutes (FAS visits timeout after 20)

fasurl = tg.config.get('fedoracommunity.connector.fas.baseurl')
fas_cache = Cache('fas_repozewho_cache', type="memory")

def fas_make_who_middleware(app, log_stream):
    faswho = FASWhoPlugin(fasurl)
    csrf_mdprovider = CSRFMetadataProvider(
            login_handler=tg.config.get('moksha.csrf.login_handler', '/login_handler'))

    form = RedirectingFormPlugin('/community/login', '/login_handler', '/logout',
                                 rememberer_name='fasident',
                                 reason_param='ec')
    form.classifications = { IIdentifier:['browser'],
                             IChallenger:['browser'] } # only for browser

    identifiers = [('form', form),('fasident', faswho)]
    authenticators = [('fasauth', faswho)]
    challengers = [('form',form)]
    mdproviders = [('fasmd', faswho), ('csrfmd', csrf_mdprovider)]

    if os.environ.get('FAS_WHO_LOG'):
        log_stream = sys.stdout

    app = PluggableAuthenticationMiddleware(
        app,
        identifiers,
        authenticators,
        challengers,
        mdproviders,
        default_request_classifier,
        default_challenge_decider,
        log_stream = log_stream
        )

    return app

class FasClient(ProxyClient):

    def __init__(self, baseURL):
        check_certs = tg.config.get('fedora.clients.check_certs', 'True').lower()
        if check_certs in ('false', '0', 'no'):
            insecure = True
        else:
            # fail safe
            insecure = False

        super(FasClient, self).__init__(baseURL,
                                        session_as_cookie=False,
                                        insecure=insecure)

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

        try:
            del(result[1]['person']['password'])
        except:
            pass

        return result

class FASWhoPlugin(object):
    def __init__(self, url, session_cookie='authtkt'):
        self.url = url
        self.session_cookie = session_cookie
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

        cookie = req.cookies.get(self.session_cookie)

        if cookie is None:
            return None

        log.info("Request identify for cookie " + cookie)
        linfo = fas_cache.get_value(key=cookie + "_identity",
                                    createfunc=lambda: self.keep_alive(cookie),
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

            return me
        except Exception, e:
            log.warning(e)
            return None

    def remember(self, environ, identity):
        log.info('Remeber')

        result = []
        req = webob.Request(environ)

        linfo = environ.get('FAS_LOGIN_INFO')
        if isinstance(linfo, tuple):
            session_id = linfo[0]
            set_cookie = '%s=%s; Path=/;' % (self.session_cookie, session_id)
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
            expired = '%s=""; Path=/; Expires=Sun, 10-May-1971 11:59:00 GMT' % self.session_cookie
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

        err_goto = '/login'
        default_came_from = '/'
        if 'SCRIPT_NAME' in environ:
            sn = environ['SCRIPT_NAME']
            err_goto = sn + err_goto
            default_came_from = sn + default_came_from

        query = parse_dict_querystring(environ)
        form = parse_formvars(environ)
        form.update(query)
        came_from = form.get('came_from', default_came_from)

        user_data = ""
        try:
            fas = FasClient(self.url)
            user_data = fas.login(login, password)
        except AuthError, e:
            log.info('Authentication failed, setting error')
            log.warning(e)
            err = 1
            environ['FAS_AUTH_ERROR'] = err

            err_app = HTTPFound(err_goto + '?' +
                                'came_from=' + quote_plus(came_from) +
                                '&ec=' + login_err.USERNAME_PASSWORD_ERROR.code)

            environ['repoze.who.application'] = err_app

            return None

        if user_data:
            if isinstance(user_data, tuple):
                environ['FAS_LOGIN_INFO']=fas.keep_alive(user_data[0], True)
                # let the csrf plugin know we just authenticated and it needs
                # to rewrite the redirection app
                environ['CSRF_AUTH_SESSION_ID'] = environ['FAS_LOGIN_INFO'][0]
                return login

        err = 'An unknown error happened when trying to log you in.  Please try again.'
        environ['FAS_AUTH_ERROR'] = err
        err_app = HTTPFound(err_goto + '?' +
                                'came_from=' + came_from +
                                '&ec=' + login_err.UNKNOWN_AUTH_ERROR.code)

        environ['repoze.who.application'] = err_app

        return None

    def get_metadata(self, environ):
        log.info("Metadata cache miss - refreshing metadata")
        info = environ.get('FAS_LOGIN_INFO')
        identity = {}

        if info is not None:
            identity.update(info[1])
            identity['session_id'] = info[0]

        for plugin in self._metadata_plugins:
            plugin(identity)

        # we don't define permissions since we don't
        # have any peruser data though other services
        # may wish to add another metadata plugin to do so

        if not identity.has_key('permissions'):
            identity['permissions'] = set()

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

        cookie = req.cookies.get(self.session_cookie)

        if cookie is None:
            # @@ Should we resort to this?
            #cookie = environ.get('CSRF_AUTH_SESSION_ID')
            return None

        log.info('Request metadata for cookie %s' % (cookie))
        info = fas_cache.get_value(key=cookie + '_metadata',
                                   createfunc=lambda: self.get_metadata(environ),
                                   expiretime=FAS_CACHE_TIMEOUT)

        identity.update(info)

        if 'repoze.what.credentials' not in environ:
            environ['repoze.what.credentials'] = {}

        environ['repoze.what.credentials']['groups'] = info['groups']
        environ['repoze.what.credentials']['permissions'] = info['permissions']

        # Adding the userid:
        userid = identity['repoze.who.userid']
        environ['repoze.what.credentials']['repoze.what.userid'] = userid

    def __repr__(self):
        return '<%s %s>' % (self.__class__.__name__, id(self))


"""
We don't need any of this, we simply need to set identity['groups']
and identity['permissions'] in our who metadata layer I'm leaving
this skeleton here just incase we do want to implement getting the
whole FAS database (we don't though)

from repoze.what.adapters import BaseSourceAdapter

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
