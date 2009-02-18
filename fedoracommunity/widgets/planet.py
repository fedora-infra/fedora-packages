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
from moksha.api.widgets.feed import LiveFeedWidget

class PlanetFedoraWidget(LiveFeedWidget):
    url = 'http://planet.fedoraproject.org/atom.xml'
    css = [CSSLink(link='/css/planet-fedora-bubbles.css')]
    limit = 3
    engine_name = 'mako'
    template = """
<div id="${id}" class="list">
    <h3><a href="http://planet.fedoraproject.org">Planet Fedora</a></h3>

    % for entry in feed.iterentries(d=d, limit=limit):
        <div class="entry">
            <div id="${entry['uid']}">
                <div id="${entry['uid']}_person" class="person-info">
                         <img src="${entry.author_detail.get('hackergotchi', 'http://planet.fedoraproject.org/images/heads/default.png')}" height="40" />
                    <a title="${entry.author_detail.name}'s blog" href="${entry.author_detail.href}"> 
                         ${entry.author_detail.name}
                    </a>
                </div>
                <div class="post">
                    <div class="post-header">
                        <h3 class="post-title">
                            <a href="${entry.link}" target="_blank">${entry.title}</a></span>
                        </h3>
                    </div>
                    <div class="post-contents" id="${entry['uid']}_text">
                        ${entry.content[0].value}
                    </div>
                    <div class="post-footer">
                    </div>
                    <b class="vt lt">&nbsp;</b>
                    <b class="vt rt">&nbsp;</b>
                    <b class="hz to">&nbsp;</b>
                    <b class="hz bo">&nbsp;</b>
                    <b class="cr tl">&nbsp;</b>
                    <b class="cr tr">&nbsp;</b>
                    <b class="cr bl">&nbsp;</b>
                    <b class="cr br">&nbsp;</b>
                </div>
            </div>
        </div>
        <script>

            hackergochi = $("#${entry['uid']}_text img:first");
            if (hackergochi) {
                $("#${entry['uid']}_person img:first").remove();
                $("#${entry['uid']}_person").prepend($("#${entry['uid']}_text img:first"));
            }

        </script>
    % endfor
</div>
    """
    #javascript = [JSLink(link='/javascript/jquery.jtruncate.js')]
    #template = "mako:fedoracommunity.widgets.templates.planet"
