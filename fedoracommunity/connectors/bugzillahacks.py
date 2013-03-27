""" Crazy hacks to make bugzilla work without throwing SSL timeouts. """

import sys


# If we're not on python2.7, we assume we're on python2.6.
PY27 = (
    sys.version_info[0] == 2 and
    sys.version_info[1] == 7
)


def hotpatch_bugzilla():
    """ Hotpatch or "duck-punch" bugzilla.base.SafeCookieTransport
    to use a longer timeout with xmlrpclib.  When we ask for "all
    the bugs on the kernel ever", it can take a long time.
    """
    import httplib
    import bugzilla.base

    # This is in seconds.  120 seconds is two minutes.
    longer_timeout = 120

    if PY27:
        # In the case of python2.7 we apply a hot patch to python-bugzilla's
        # SafeCookieTransport and have it pass in an SSL timeout to xmlrpclib.
        def patched_make_connection(self, host):
            if self._connection and host == self._connection[0]:
                return self._connection[1]
            # create a HTTPS connection object from a host descriptor
            # host may be a string, or a (host, x509-dict) tuple
            try:
                HTTPS = httplib.HTTPSConnection
            except AttributeError:
                raise NotImplementedError(
                    "your version of httplib doesn't support HTTPS"
                )
            else:
                chost, self._extra_headers, x509 = self.get_host_info(host)
                self._connection = host, HTTPS(
                    chost,
                    None,
                    timeout=longer_timeout,
                    **(x509 or {})
                )
                return self._connection[1]

        # In bugzilla-0.8.0 this transport class got renamed out from under us.
        if bugzilla.version == '0.7.0':
            bugzilla.base.SafeCookieTransport.make_connection = \
                patched_make_connection
        else:
            bugzilla.base._CookieTransport.make_connection = \
                patched_make_connection

    else:
        # In the case of python2.6, we have to do something different and apply
        # a hot patch to the stdlib's httplib since xmlrpclib is written
        # against an ancient backwards compatible version of httplib.
        # (python-2.6's xmlrpclib is compatible with python-1.5's httplib.
        # Crazy!)
        def __init__(self, host='', port=None, key_file=None, cert_file=None,
                     strict=None):
            # provide a default host, pass the X509 cert info

            # urf. compensate for bad input.
            if port == 0:
                port = None
            self._setup(self._connection_class(host, port, key_file,
                                               cert_file, strict,
                                               timeout=longer_timeout))

            # we never actually use these for anything, but we keep them
            # here for compatibility with post-1.5.2 CVS.
            self.key_file = key_file
            self.cert_file = cert_file

        httplib.HTTPS.__init__ = __init__
