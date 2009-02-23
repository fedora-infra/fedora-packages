from repoze.who.middleware import PluggableAuthenticationMiddleware
from repoze.who.interfaces import IChallenger, IIdentifier
from repoze.who.plugins.form import RedirectingFormPlugin

from hashlib import sha1
from webob import Request

from paste.request import construct_url
from paste.httpexceptions import HTTPFound
from paste.request import parse_formvars
from paste.request import parse_dict_querystring
from paste.response import replace_header

from urlparse import urlparse, urlunparse

import logging

log = logging.getLogger(__name__)

class CSRFWhoPlugin(object):
    def __init__(self, session_id, csrf_token_id):
        self.session_id = session_id
        self.csrf_token_id = csrf_token_id

    def add_metadata(self, environ, identity):
        """
        Generate the sha1 of tg-visit and add set identity._csrf_token
        """

        log.info('Metadata')

        req = Request(environ)
        session_id = req.cookies.get(self.session_id)

        if session_id is None:
            return None

        token = sha1(session_id)
        token = token.hexdigest()
        info = {self.csrf_token_id: token}

        identity.update(info)

        # check for csrf
        # hack to remove csrf variable from environ
        csrf_check = None
        d = parse_dict_querystring(environ)
        if self.csrf_token_id in d:
            csrf_check = d.getone(self.csrf_token_id)
            d.__delitem__(self.csrf_token_id)

            qs = []
            for k in d:
                qs.append('%s=%s'%(k,d[k]))

            qs = '&'.join(qs)
            environ['QUERY_STRING'] = qs

        d = parse_formvars(environ, False)
        if self.csrf_token_id in d:
            csrf_check = d.getone(self.csrf_token_id)
            d.__delitem__(self.csrf_token_id)
            environ['paste.parsed_formvars'] = d

        session_id = environ.get('CSRF_AUTH_SESSION_ID', False)
        if (session_id):
            log.info(dir(environ['repoze.who.application']))
            app = environ['repoze.who.application']
            token = sha1(session_id).hexdigest()
            p = list(urlparse(app.location()))
            p[4] += '&' + self.csrf_token_id + '=' + token
            replace_header(app.headers, 'location', urlunparse(tuple(p)))

        else:
            if token != csrf_check and 'repoze.what.credentials' in environ:
                del environ['repoze.what.credentials']

    def __repr__(self):
        return '<%s %s>' % (self.__class__.__name__, id(self))
