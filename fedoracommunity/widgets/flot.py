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

from tw.api import Widget
from tw.jquery import jQuery, jquery_js
from tw.jquery.flot import flot_css, flot_js, excanvas_js

class FlotWidget(Widget):
    """ An attractive plotting widget.

    Using Flot, a pure Javascript plotting library for jQuery,
    this widget produces client-side graphical plots of arbitrary datasets
    on-the-fly.

    For detailed documentation on the flot API, visit the flot project 
    homepage: http://code.google.com/p/flot
    """
    template = u"""
        % if label:
          <h3>${label}</h3>
        % endif
        <div id="${id}" style="width:${width};height:${height};">
        </div>
        <script>
            $(document).ready(function(){
                if (!${data}) {
                    $('#${id}').text('Data not ready for display \u2014 sorry!');
                } else {
                    $.plot($('#${id}'), ${data}, ${options});
                }
            });
        </script>
    """
    engine_name = 'mako'
    params = {
            "data"    : "An array of data series",
            "options" : "Plot options",
            "height"  : "The height of the graph",
            "width"   : "The width of the graph",
            "label"   : "Label for the graph",
            "id"      : "An optional ID for the graph"
    }
    javascript = [jquery_js, flot_js, excanvas_js]
    css = [flot_css]
    height = '300px'
    width = '600px'
    label = ''

    def update_params(self, d):
        super(FlotWidget, self).update_params(d)
        if not d.get('id'):
            d['id'] = 'flot_%s' % str(int(random() * 999))
        data = d.get('data') or []
        options = d.get('options') or {}
        return d
