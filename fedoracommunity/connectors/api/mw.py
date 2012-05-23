# This file is part of Moksha.
# Copyright (C) 2008-2010  Red Hat, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Authors: John (J5) Palmieri <johnp@redhat.com>

import logging
import pkg_resources
import urllib
import time
import os.path
import threading

try:
    import json
except ImportError:
    import simplejson as json

from paste.deploy.converters import asbool
from webob import Request, Response
from pprint import pformat
from tg import config

log = logging.getLogger(__name__)

class FCommConnectorMiddleware(object):
    """
    A layer of WSGI middleware that is responsible for handling every
    fcomm_connector requests.

    If a request for a connector comes in (/fcomm_connector/$name), it will
    run that connector as defined in it's egg-info.

    """

    _connectors = {}
    profile_id_counter = 0
    profile_id_counter_lock = threading.Lock()

    def __init__(self, application):
        log.info('Creating FCommConnectorMiddleware')
        self.application = application

        # ids of profile data we are waiting to collect and record
        self.outstanding_profile_ids = {}

        self.load_connectors()

    def strip_script(self, environ, path):
        # Strips the script portion of a url path so the middleware works even
        # when mounted under a path other than root
        if path.startswith('/') and 'SCRIPT_NAME' in environ:
            prefix = environ.get('SCRIPT_NAME')
            if prefix.endswith('/'):
                prefix = prefix[:-1]

            if path.startswith(prefix):
                path = path[len(prefix):]

        return path

    def prof_collector(self, environ, request, start_response):
        p = request.params
        profile_id = p['id']
        directory = config.get('profile.dir', '')
        if self.outstanding_profile_ids.pop(profile_id, False):
            prof_file_name = "jsonrequest_%s.jsprof" % profile_id

            # output profiling data
            file_name = os.path.join(directory, prof_file_name)
            f = open(file_name, 'w')
            f.write('{"id": "%s", "start_time": %s, "callback_start_time": %s, "end_time": %s}'
                    % (profile_id, p['start_time'], p['callback_start_time'], p['end_time']))
            f.close()
            return Response('{}')(environ, start_response)

        return Response(status='404 Not Found')(environ, start_response)

    def __call__(self, environ, start_response):

        request = Request(environ)

        path = self.strip_script(environ, request.path)
        if path.startswith('/fcomm_connector'):
            s = path.split('/')[2:]

            # check to see if we need to hand this off to the profile collector
            if s[0] == 'prof_collector':
                return self.prof_collector(environ, request, start_response)

            # since keys are not unique we need to condense them
            # into an actual dictionary with multiple entries becoming lists
            p = request.params
            params = {}
            for k in p.iterkeys():
                if k == '_cookies':
                    # reserved parameter
                    # FIXME: provide a proper error response
                    return Response(status='404 Not Found')

                if k not in params:
                    params[k] = p.getall(k)
                    if params[k] and len(params[k]) == 1:
                        params[k] = params[k][0]

            try:
                response = self._run_connector(environ, request,
                                               s[0], s[1], *s[2:],
                                               **params)
            except IndexError, e:
                log.info('Invalid connector path: %s' % str(e))
                return Response(status='404 Not Found')(environ, start_response)
        else:
            response = request.get_response(self.application)

        return response(environ, start_response)

    def _run_connector(self, environ, request,
                       conn_name, op, *path,
                       **remote_params):
        response = None
        # check last part of path to see if it is json data
        dispatch_params = {};

        if len(path) > 0:
            p = urllib.unquote_plus(path[-1].lstrip())
            if p.startswith('{'):
                dp = json.loads(p)

                f = dp.get('filters')
                if isinstance(f, basestring):
                    dp['filters'] = json.loads(f)
                path = path[:-1]

                # scrub dispatch_params keys of unicode so we can pass as keywords
                for (k, v) in dp.iteritems():
                    dispatch_params[str(k)] = v

            # prevent trailing slash
            if not p:
                path = path[:-1]

            path = '/'.join(path)
        else:
            path = ''

        conn = self._connectors.get(conn_name)

        # pretty print output
        pretty_print = False

        if '_pp' in remote_params:
            del remote_params['_pp']
            pretty_print = True

        if conn:
            conn_obj = conn['connector_class'](environ, request)

            r = None
            if asbool(config.get('profile.connectors')):
                try:
		    import cProfile as profile
                except ImportError:
                    import profile
                directory = config.get('profile.dir', '')

                # Make sure the id is unique for each thread
                self.profile_id_counter_lock.acquire()
                prof_id_counter = self.profile_id_counter
                self.profile_id_counter += 1
                self.profile_id_counter_lock.release()

                ip = request.remote_addr
                timestamp = time.time()

                profile_id = "%s_%f_%s_%i" % (conn_name, timestamp, ip, prof_id_counter)
                self.outstanding_profile_ids[profile_id] = True
                prof_file_name = "connector_%s.prof" % profile_id
                info_file_name = "connector_%s.info" % profile_id

                # output call info
                file_name = os.path.join(directory, info_file_name)
                f = open(file_name, 'w')
                f.write('{"name": "%s", "op": "%s", "path": "%s", "remote_params": %s, "ip": "%s", "timestamp": %f, "id_counter": %i, "id": "%s"}'
                    % (conn_name, op, path, json.dumps(remote_params), ip, timestamp, prof_id_counter, profile_id))
                f.close()

                # in order to get the results back we need to pass an object
                # by refrence which will be populated with the actual results
                result = {'r': None}

                # profile call
                file_name = os.path.join(directory, prof_file_name)
                profile.runctx("result['r'] = conn_obj._dispatch(op, path, remote_params, **dispatch_params)",
                                None,
                                {'conn_obj': conn_obj,
                                 'op': op,
                                 'path': path,
                                 'remote_params': remote_params,
                                 'dispatch_params': dispatch_params,
                                 'result': result},
                                file_name)

                r = result['r']

                # add profile id to results
                r['moksha_profile_id'] = profile_id
            else:
                r = conn_obj._dispatch(op, path, remote_params, **dispatch_params)

            if pretty_print:
                r = '<pre>' + pformat(r) + '</pre>'
            elif not isinstance(r, basestring):
                r = json.dumps(r, separators=(',',':'))

            if isinstance(r, unicode):
                r = r.encode('utf-8', 'replace')

            response = Response(r)
        else:
            response = Response(status='404 Not Found')

        return response

    def load_connectors(self):
        log.info('Loading fcomm connectors')
        for conn_entry in pkg_resources.iter_entry_points('fcomm.connector'):
            log.info('Loading %s connector' % conn_entry.name)
            conn_class = conn_entry.load()
            # call the register class method
            # FIXME: Should we pass some resource in?
            conn_class.register()
            conn_path = conn_entry.dist.location
            self._connectors[conn_entry.name] = {
                    'name': conn_entry.name,
                    'connector_class': conn_class,
                    'path': conn_path,
                    }

def _get_connector(name, request=None):
    # TODO: having a connection pool might be nice
    cls = None
    if name in FCommConnectorMiddleware._connectors:
        cls = FCommConnectorMiddleware._connectors[name]['connector_class']
    else:
        # Look for it on the entry-point
        for conn_entry in pkg_resources.iter_entry_points('fcomm.connector'):
            if conn_entry.name == name:
                conn_class = conn_entry.load()
                conn_class.register()
                cls = conn_class

    if request is None:
        from pylons import request

    if cls:
        try:
            return cls(request.environ, request)
        except TypeError:
            # Called outside of the WSGI stack
            return cls(None, None)
