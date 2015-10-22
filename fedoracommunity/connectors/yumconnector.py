# This file is part of Fedora Community.
# Copyright (C) 2008-2014  Red Hat, Inc.
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

from fedoracommunity.connectors.api import (
    IConnector,
    ICall,
    IQuery,
)

import requests

from tg import config

import os
import re


class YumConnector(IConnector, ICall, IQuery):
    """ SURPRISE!  This doesn't really use yum anymore.

    It uses mdapi.

    """
    _method_paths = {}
    _query_paths = {}
    fedora_base_repo_re = re.compile('Fedora ([0-9]+)$')

    def __init__(self, environ=None, request=None):
        super(YumConnector, self).__init__(environ, request)

    # IConnector
    @classmethod
    def register(cls):
        cls._mdapi_url = config.get('fedoracommunity.connector.mdapi.url',
                                    'http://209.132.184.236')  # dev instance
        cls.register_method('get_file_tree', cls.call_get_file_tree)

    def introspect(self):
        # FIXME: return introspection data
        return None

    def _add_to_path(self, paths_cache, path, data):
        if path == '':
            path = '/'

        if path in paths_cache:
            dir_info = paths_cache[path]
            if data:
               dir_info['children'].append(data)
            return

        new_data = {
                    'data': {
                          'title': '',
                          'icon': 'jstree-directory'
                       },
                     'state': 'open',
                     'children': []
                   }
        if data:
           new_data['children'].append(data)
        paths_cache[path] = new_data
        (new_path, dir_name) = os.path.split(path)
        new_data['data']['title'] = dir_name
        self._add_to_path(paths_cache, new_path, new_data)

    def _process_files(self, data):
        paths_cache = {'/':{'children':[]}}

        for entry in data:
            self._add_to_path(paths_cache, entry['dirname'], None)

            filenames = entry['filenames'].split('/')
            filenames = zip(filenames, entry['filetypes'])
            for filename, type in filenames:
                output = {
                    'name': filename,
                    'path': entry['dirname'],
                    'display_size': None,
                    'type': type.upper(),
                    'modestring': '',
                    'linked_to': None,
                    'user': None,
                    'group': None,
                    # jsTree JSON data
                    'data': {
                        'title': filename,
                        'icon': 'jstree-file'
                    },
                    'state': 'open',
                }

                # construct directory structure
                self._add_to_path(paths_cache, entry['dirname'], output)

        return paths_cache['/']['children']

    def call_get_file_tree(self, resource_path=None, _cookies=None, package=None, repo='rawhide', arch=None):
        repo = repo.lower()
        url = '/'.join([self._mdapi_url, repo, 'files', package])
        response = requests.get(url)
        if not bool(response):
            return {
                'error': 'Could not find package in mdapi.',
            }

        try:
            result = self._process_files(response.json())
        except Exception as e:
            result = {'error': "Error: %s" % str(e)}

        return result
