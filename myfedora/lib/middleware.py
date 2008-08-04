# -*- coding: utf-8 -*-
#
# Copyright © 2007-2008  Red Hat, Inc. All rights reserved.
#
# This copyrighted material is made available to anyone wishing to use, modify,
# copy, or redistribute it subject to the terms and conditions of the GNU
# General Public License v.2.  This program is distributed in the hope that it
# will be useful, but WITHOUT ANY WARRANTY expressed or implied, including the
# implied warranties of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.  You should have
# received a copy of the GNU General Public License along with this program;
# if not, write to the Free Software Foundation, Inc., 51 Franklin Street,
# Fifth Floor, Boston, MA 02110-1301, USA. Any Red Hat trademarks that are
# incorporated in the source code or documentation are not subject to the GNU
# General Public License and may only be used or replicated with the express
# permission of Red Hat, Inc.
#
# Author(s): Toshio Kuratomi <tkuratom@redhat.com>
#            Ricky Zhou <ricky@fedoraproject.org>
#            John (J5) Palmieri <johnp@redhat.com>
#
# Adapted from code in python-fedora
#



import Cookie

from myfedora.lib.utils import pretty_print_map, pretty_print_array
from fedora.client import BaseClient, FedoraServiceError

from fedora import _

import crypt

import paste
import webob
from webob.exc import *

import logging
log = logging.getLogger('turbogears.identity.safasprovider')

try:
    # pylint: disable-msg=W0104
    set, frozenset
except NameError:
    from sets import Set as set                 # pylint: disable-msg=W0622
    from sets import ImmutableSet as frozenset  # pylint: disable-msg=W0622

class DictContainer(dict):
    '''Dictionary that also works from attribute lookups.'''
    def __init__(self, basedict):
        super(DictContainer, self).__init__()
        for key in basedict:
            if type(basedict[key]) == dict:
                self[key] = DictContainer(basedict[key])
            else:
                self[key] = basedict[key]

    def __getattr__(self, attr):
        try:
            return self[attr]
        except KeyError, e:
            raise AttributeError, _(
                    "'%(name)s' object has no attribute '%(attr)s'") \
                    %{'name': self.__class__.__name__, 'attr': e.message}

class JsonFasIdentity(BaseClient):
    '''
    This middleware provides integration with the Fedora Account
    System using JSON calls.
    
    Associate an identity with a person in the auth system.
    '''
    cookie_name = 'tg-visit'
    fas_url = 'https://localhost:8088/accounts/'

    def __init__(self, visit_key, user=None, username=None, password=None,
            debug=False):
        super(JsonFasIdentity, self).__init__(self.fas_url, debug=debug)
        if user:
            self._user = user
            self._groups = frozenset(
                    [g['name'] for g in user['approved_memberships']]
                    )
        self.visit_key = visit_key
        # It's allowed to use a null value for a visit_key if we know we're
        # generating an anonymous user.  The json interface doesn't handle
        # that, though, and there's no reason for us to make it.
        if not visit_key:
            return

        # Set the cookie to the user's tg_visit key before requesting
        # authentication.  That way we link the two together.
        self._session_cookie = Cookie.SimpleCookie()
        self._session_cookie[self.cookie_name] = visit_key
        response.simple_cookie[self.cookie_name] = visit_key

        self.username = username
        self.password = password
        if username and password:
            self._authenticate(force=True)

    def _authenticate(self, force=False):
        '''Override BaseClient so we can keep visit_key in sync.
        '''
        super(JsonFasIdentity, self)._authenticate(force)
        if self._session_cookie[self.cookie_name].value != self.visit_key:
            # When the visit_key changes (because the old key had expired or
            # been deleted from the db) change the visit_key in our variables
            # and the session cookie to be sent back to the client.
            self.visit_key = self._session_cookie[self.cookie_name].value
            response.simple_cookie[self.cookie_name] = self.visit_key
        return self._session_cookie
    session = property(_authenticate)

    def _get_user(self):
        '''Retrieve information about the user from cache or network.'''
        # pylint: disable-msg=W0704
        try:
            return self._user
        except AttributeError:
            # User hasn't already been set
            pass
        # pylint: enable-msg=W0704
        # Attempt to load the user. After this code executes, there *WILL* be
        # a _user attribute, even if the value is None.
        # Query the account system URL for our given user's sessionCookie
        # FAS returns user and group listing
        # pylint: disable-msg=W0702
        try:
            data = self.send_request('user/view', auth=True)
        except:
            # Any errors have to result in no user being set.  The rest of the
            # framework doesn't know what to do otherwise.
            self._user = None
            return None
        # pylint: enable-msg=W0702
        if not data['person']:
            self._user = None
            return None
        self._user = DictContainer(data['person'])
        self._groups = frozenset(
                [g['name'] for g in data['person']['approved_memberships']]
                )
        return self._user
    user = property(_get_user)

    def _get_user_name(self):
        '''Return the username for the user.'''
        if not self.user:
            return None
        return self.user['username']
    user_name = property(_get_user_name)

    def _get_anonymous(self):
        '''Return True if there's no user logged in.'''
        return not self.user
    anonymous = property(_get_anonymous)

    def _get_display_name(self):
        '''Return the user's display name.'''
        if not self.user:
            return None
        return self.user['human_name']
    display_name = property(_get_display_name)

    def _get_groups(self):
        '''Return the groups that a user is a member of.'''
        try:
            return self._groups
        except AttributeError:
            # User and groups haven't been returned.  Since the json call
            # returns both user and groups, this is set at user creation time.
            self._groups = frozenset()
        return self._groups
    groups = property(_get_groups)

    def logout(self):
        '''
        Remove the link between this identity and the visit.
        '''
        if not self.visit_key:
            return
        # Call Account System Server logout method
        self.send_request('logout', auth=True)

class JsonFasMiddleware(object):
    '''
    IdentityProvider that authenticates users against the fedora account system
    '''
    def __init__(self, app, config):
        
        # Default encryption algorithm is to use plain text passwords
        self.app = app
        algorithm = config.get('identity.saprovider.encryption_algorithm', None)
        self.encrypt_password = lambda pw: \
                             identity._encrypt_password(algorithm, pw)
        self.remote_user_key = 'REMOTE_USER'

    def __call__(self, environ, start_response):
        print "jsonfas middleware: "
        req = webob.Request(environ)
        resp_app = self.app

        #pretty_print_map(environ)

        if self.remote_user_key in environ:
            # act as a pass through if REMOTE_USER (or whatever) is
            # already set
            return self.app(environ, start_response)

        path_info = environ.get('PATH_INFO', None)

        environ['jsonfas.application'] = self.app

        if environ['PATH_INFO'] == '/login_handler':
            print environ['QUERY_STRING']
            go_to = req.GET.get('came_from', '/');
            print go_to
            exc = HTTPSeeOther(location=go_to)
            resp_app = exc
            
        resp = req.get_response(resp_app)
        
        userid = None
        identity = None
        identifier = None

        return resp(environ, start_response)


    def validate_identity(self, user_name, password, visit_key):
        '''
        Look up the identity represented by user_name and determine whether the
        password is correct.

        Must return either None if the credentials weren't valid or an object
        with the following properties:
            user_name: original user name
            user: a provider dependant object (TG_User or similar)
            groups: a set of group IDs
            permissions: a set of permission IDs
        '''
        try:
            user = JsonFasIdentity(visit_key, username = user_name,
                    password = password)
        except FedoraServiceError, e:
            log.warning(_('Error logging in %(user)s: %(error)s') % {
                'user': user_name, 'error': e})
            return None

        return user

    def validate_password(self, user, user_name, password):
        '''
        Check the supplied user_name and password against existing credentials.
        Note: user_name is not used here, but is required by external
        password validation schemes that might override this method.
        If you use SqlAlchemyIdentityProvider, but want to check the passwords
        against an external source (i.e. PAM, LDAP, Windows domain, etc),
        subclass SqlAlchemyIdentityProvider, and override this method.

        Arguments:
        :user: User information.  Not used.
        :user_name: Given username.
        :password: Given, plaintext password.

        Returns: True if the password matches the username.  Otherwise False.
          Can return False for problems within the Account System as well.
        '''
        
        return user.password == crypt.crypt(password, user.password)

    def load_identity(self, visit_key):
        '''Lookup the principal represented by visit_key.

        Arguments:
        :visit_key: The session key for whom we're looking up an identity.

        Must return an object with the following properties:
            user_name: original user name
            user: a provider dependant object (TG_User or similar)
            groups: a set of group IDs
            permissions: a set of permission IDs
        '''
        return JsonFasIdentity(visit_key)

    def anonymous_identity(self):
        '''
        Must return an object with the following properties:
            user_name: original user name
            user: a provider dependant object (TG_User or similar)
            groups: a set of group IDs
            permissions: a set of permission IDs
        '''
        return JsonFasIdentity(None)

    def authenticated_identity(self, user):
        '''
        Constructs Identity object for user that has no associated visit_key.
        '''
        return JsonFasIdentity(None, user)
        
class Identity(dict):
    """ dict subclass that prevents its members from being rendered
    during print """
    def __repr__(self):
        return '<repoze.who identity (hidden, dict-like) at %s>' % id(self)
    __str__ = __repr__

import pylons