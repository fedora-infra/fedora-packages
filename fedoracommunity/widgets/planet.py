# This file is part of Fedora Community
#
# Fedora Community is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Fedora Community is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Fedora Community If not, see <http://www.gnu.org/licenses/>.
#
# Copyright 2008, Red Hat, Inc.

"""
:mod:`fedoracommunity.widgets.planet` -- Planet Fedora Widget
=============================================================

.. module:: fedoracommunity.widgets.planet
.. moduleauthor:: Luke Macken <lmacken@redhat.com>
"""

from tw.api import CSSLink, JSLink
from moksha.api.widgets.feed import Feed

class PlanetFedoraWidget(Feed):
    url = 'http://planet.fedoraproject.org/atom.xml'
    template = "mako:fedoracommunity.widgets.templates.planet"
    javascript = [JSLink(link='/javascript/jquery.expander.js')]
    css = [CSSLink(link='/css/planet-fedora-bubbles.css')]
    params = ['limit']
    limit = 3
