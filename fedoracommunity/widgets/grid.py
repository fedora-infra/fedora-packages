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

import uuid
import simplejson as json

from tg import config
from paste.deploy.converters import asbool

import tw2.core as twc
import tw2.forms
import tw2.jquery
import tw2.jqplugins.ui

from moksha.wsgi.lib.helpers import when_ready
from fedoracommunity.widgets.jquery_template import jquery_template_js

moksha_ui_grid_js = twc.JSLink(
    filename='static/javascript/ui/moksha.ui.grid.js',
    modname=__name__,
    resources=[
        tw2.jqplugins.ui.jquery_ui_js,
        jquery_template_js,
    ],
)

moksha_ui_popup_js = twc.JSLink(
    filename='static/javascript/ui/moksha.ui.popup.js',
    modname=__name__,
    resources=[
        tw2.jqplugins.ui.jquery_ui_js,
    ],
)


class Grid(tw2.forms.widgets.FormField):
    resources = [tw2.jqplugins.ui.jquery_ui_js,
                 moksha_ui_grid_js,
                 moksha_ui_popup_js]
    params= ['rows_per_page', 'page_num', 'total_rows',
            'filters', 'unique_key', 'sort_key', 'sort_order',
            'row_template', 'resource', 'resource_path',
            'loading_throbber', 'uid', 'more_link']
    hidden = True # hide from the moksha main menu

    id = twc.Param(default=None)
    rows_per_page = twc.Param(default=10)
    page_num = twc.Param(default=1)
    total_rows = twc.Param(default=0)
    filters = twc.Param(default=None)
    unique_key = twc.Param(default=None)
    sort_key = twc.Param(default=None)
    sort_order = twc.Param(default=-1)
    row_template = twc.Param(default=None)
    resource = twc.Param(default=None)
    resource_path = twc.Param(default=None)
    loading_throbber = twc.Param(default=None)
    uid = twc.Param(default=None)
    more_link = twc.Param(default=None)
    onReady = None

    def prepare(self):
        """
        Subclasses *must* call super as the last thing in their prepare() method
        """
        super(Grid, self).prepare()

        if not self.filters:
            self.filters = {}

        grid_d = {}
        for p in self.params:
            v = getattr(self, p)
            if v is not None:
                grid_d[p] = v

        self.id = self.__class__.__name__ + str(uuid.uuid4())

        onready = getattr(self, 'onReady')
        if onready:
            grid_d['loadOnCreate'] = False

        if onready:
            self.add_call(when_ready("%s; %s;" % (tw2.jquery.jQuery("#%s" % self.id).mokshagrid(grid_d), onready)))
        else:
            self.add_call(when_ready(tw2.jquery.jQuery("#%s" % self.id).mokshagrid(grid_d)))
