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



from Cookie import SimpleCookie

from myfedora.lib.utils import pretty_print_map, pretty_print_array
from fedora.client import ProxyClient, FedoraServiceError

from fedora import _

import crypt

import paste
import webob
from webob.exc import *

import logging
log = logging.getLogger('turbogears.identity.safasprovider')

fasurl = 'https://admin.fedoraproject.org/accounts'

class FasClient(ProxyClient):
    visit_name = 'tg-visit'
    
    def __init__(self, baseURL, visit_cookie=None):
        super(FasClient, self).__init__(baseURL)
        self.visit_cookie = visit_cookie

    def login(self, ident):
        return self.send_request("login", 
                                 auth_params={'username': ident['username'], 
                                              'password':ident['password']})
        
    def logout(self):
        auth_params = {}
        if self.visit_cookie:
            auth_params = {'cookie': self.visit_cookie}
            
        return self.send_request("logout", auth_params = auth_params)

class FasMiddleware(object):
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
        req = webob.Request(environ)
        resp_app = self.app

        #pretty_print_map(environ)

        path_info = environ.get('PATH_INFO', None)

        environ['fas.application'] = self.app

        session_id = req.cookies.get('session_id', None)
        tg_visit = req.cookies.get('tg_visit', None)
        
        sc = SimpleCookie()
        for key, value in req.cookies.iteritems():
            sc[key] = value
        
        fas = FasClient(fasurl, sc)

        path_info = environ['PATH_INFO']
        if path_info[-1] == '/':
            path_info = path_info[:-1]
            
        if path_info == '/login_handler' or :
            ident = Identity(username=req.params['login'],
                             password=req.params['password'])
            
            
            r = fas.login(ident)
            sc = r[0]
            
            go_to = req.GET.get('came_from', '/');
            exc = HTTPSeeOther(location=go_to)
            resp_app = exc
            
        elif path_info == '/logout':
            r = fas.logout()
            sc = r[0]
            
            go_to = req.headers.get('REFERER', '/')
            exc = HTTPSeeOther(location=go_to)
            resp_app = exc
            
        resp = req.get_response(resp_app)
        resp.set_cookie('session_id', sc['session_id'])
        resp.set_cookie('tg-visit', sc['tg-visit'])
        
        userid = None
        identity = None
        identifier = None

        return resp(environ, start_response)
        
class Identity(dict):
    """ dict subclass that prevents its members from being rendered
    during print """
    def __repr__(self):
        return '<repoze.who identity (hidden, dict-like) at %s>' % id(self)
    __str__ = __repr__

import pylons