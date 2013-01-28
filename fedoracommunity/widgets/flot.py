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

import tw2.core as twc
from tw2.jquery import jQuery, jquery_js
from tw2.jqplugins.flot import flot_css, flot_js
from tw2.excanvas import excanvas_js

class FlotWidget(twc.Widget):
    """ An attractive plotting widget.

    Using Flot, a pure Javascript plotting library for jQuery,
    this widget produces client-side graphical plots of arbitrary datasets
    on-the-fly.

    For detailed documentation on the flot API, visit the flot project 
    homepage: http://code.google.com/p/flot
    """
    template = u"""
        % if w.label:
          <h3>${w.label}</h3>
        % endif
        <div id="${w.id}" style="width:${w.width};height:${w.height};">
        </div>
        <script>
        % if w.tooltips:
            function showTooltip(x, y, contents) {
                $('<div id="tooltip">' + contents + '</div>').css( {
                    position: 'absolute',
                    display: 'none',
                    top: y + 5,
                    left: x + 5,
                    border: '1px solid #fdd',
                    padding: '2px',
                    'background-color': '#fee',
                    opacity: 0.80
                }).appendTo("body").fadeIn(200);
            }

            var previousPoint = null;
            $("#${w.id}").bind("plothover", function (event, pos, item) {
                $("#x").text(pos.x.toFixed(2));
                $("#y").text(pos.y.toFixed(2));
                if (item) {
                    if (previousPoint != item.datapoint) {
                        previousPoint = item.datapoint;
                        $("#tooltip").remove();
                        var x = item.datapoint[0].toFixed(2),
                            y = item.datapoint[1].toFixed(2);
                        showTooltip(item.pageX, item.pageY, y);
                    }
                }
                else {
                    $("#tooltip").remove();
                    previousPoint = null;
                }
            });
        % endif

            $(document).ready(function(){
                if (!${w.data}) {
                    $('#${w.id}').text('Data not ready for display \u2014 sorry!');
                } else {
                    $.plot($('#${w.id}'), ${w.data}, ${w.options});
                }
            });
        </script>
    """
    inline_engine_name = 'mako'
    data = twc.Param("An array of data series", default=None)
    options = twc.Param("Plot options", default=None)
    height = twc.Param("The height of the graph", default='300px')
    width = twc.Param("The width of the graph", default='600px')
    label = twc.Param("Label for the graph", default='')
    tooltips = twc.Param("Enable onhover tooltips", default=False)

    resources = [jquery_js, flot_js, excanvas_js, flot_css]

    def prepare(self):
        super(FlotWidget, self).prepare

        if not self.id:
            self.id = 'flot_%s' % str(int(random() * 999))

        if not self.data:
            self.data = []

        if not self.options:
            self.options = {}
