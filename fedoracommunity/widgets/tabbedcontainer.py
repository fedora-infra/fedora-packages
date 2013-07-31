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


import tw2.core as twc
import tw2.forms
import tw2.jqplugins.ui

from repoze.what import predicates
from moksha.wsgi.lib.helpers import eval_app_config, ConfigWrapper, when_ready

import urllib


moksha_ui_tabs_js = twc.JSLink(
    modname='moksha',
    filename='public/javascript/ui/moksha.ui.tabs.js',
    resources=[tw2.jqplugins.ui.jquery_ui_js])


class TabbedContainerTabs(twc.Widget):
    template = 'mako:moksha.wsgi.widgets.api.containers.templates.tabbedcontainer_tabs'


class TabbedContainerPanes(twc.Widget):
    template = 'mako:moksha.wsgi.widgets.api.containers.templates.tabbedcontainer_panes'


tabwidget = TabbedContainerTabs(id='tabs')
panewidget = TabbedContainerPanes(id='panes')


class TabbedContainer(tw2.forms.widgets.FormField):
    """
    :tabs: An ordered list of application tabs to display
           Application descriptors come from the config wrappers in
           moksha.lib.helpers

           tabs can either be in serialized string format or as a list of
           config wrapper objects.  Using strings means you don't have to
           import the wrappers and predicates but can get unwieldy if there
           is a long list of wrappers

    :config_key: the configuration key used to store the serialized tab config
                 in a configuration file instead of embeding it in the widget

    :template: you must provide a template in order to get styling correct.  The
               default template has minimal functionality.  The documentation
               for jQuery.UI.Tabs can be found at http://ui.jquery.org.
               FIXME: Write a tutorial and provide helper widgets so
               creating a template becomes really easy.
    """
    template = 'mako:moksha.wsgi.widgets.api.containers.templates.tabbedcontainer'
    resources = [moksha_ui_tabs_js]

    config_key = twc.Param(default=None)
    config = twc.Param(default=None)
    tabs = twc.Param(default=())
    params = ["tabdefault", "staticLoadOnClick"]
    tabdefault = twc.Param(
        "0-based index of the tab to be selected on page load",
        default=0)
    staticLoadOnClick = twc.Param(default=False)

    def prepare(self):
        super(TabbedContainer, self).prepare()
        if not getattr(self, "id", None):
            raise ValueError("JQueryUITabs is supposed to have id")

        if self.config == None:
            self.config = {}

        o = {
            'tabdefault': self.tabdefault,
            'staticLoadOnClick': self.staticLoadOnClick
        }
        self.add_call(when_ready(
            tw2.jquery.jQuery("#%s" % self.id).mokshatabs(o)))

        tabs = eval_app_config(self.config.get(self.config_key, "None"))
        if not tabs:
            if isinstance(self.tabs, str):
                tabs = eval_app_config(self.tabs)
            else:
                tabs = self.tabs

        # Filter out any None's in the list which signify apps which are
        # not allowed to run with the current session's authorization level
        tabs = ConfigWrapper.process_wrappers(tabs, self)

        self.tabs = tabs
        self.tabwidget = tabwidget
        self.panewidget = panewidget
        self.root_id = id
