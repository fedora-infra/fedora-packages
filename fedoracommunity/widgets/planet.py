# This file is part of Fedora Community.
# Copyright (C) 2008-2010  Red Hat, Inc.
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

"""
:mod:`fedoracommunity.widgets.planet` -- Planet Fedora Widget
=============================================================

.. module:: fedoracommunity.widgets.planet
.. moduleauthor:: Luke Macken <lmacken@redhat.com>
"""

from tw2.core import CSSLink, JSLink
from moksha.api.widgets import ContextAwareWidget
from moksha.api.widgets.feed import Feed
from fedoracommunity.widgets.expander import expander_js


class PlanetFedoraWidget(Feed):
    url = 'http://planet.fedoraproject.org/atom.xml'
    template = "mako:fedoracommunity.widgets.templates.planet"
    resources = [
        expander_js,
        CSSLink(link='/community/css/planet-fedora-bubbles.css'),
    ]
    limit = twc.Param(default=3)
    def prepare(self):
        super(Feed, self).prepare()
        self.tmpl_context = pylons.tmpl_context
