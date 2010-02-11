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
MirrorManager user map viewing widget
================================

.. moduleauthor:: Luke Macken <lmacken@redhat.com>
"""

from tw.api import Widget
from tw.forms import SingleSelectField
from moksha.api.widgets.containers import DashboardContainer
from moksha.lib.helpers import Category, Widget as MokshaWidget
from moksha.api.connectors import get_connector
from fedoracommunity.widgets.imagefit import jquery_imagefit_js

class ReleaseDownloadsFilter(SingleSelectField):
    options = []
    attrs = {'onchange': """
        var release = $('#user_maps_releases').val();
        $('#maps').empty();
        if (release == 'all') {
            $('#maps').append($('<img/>').attr('src', 'http://fedoraproject.org/maps/all.png').load(function() { setTimeout(function(){ $('#maps').imagefit(); }, 100); }));
        } else {
            $('#maps').append($('<img/>').attr('src', 'http://fedoraproject.org/maps/' + release + '/' + release + '.i386.png'));
            $('#maps').append($('<img/>').attr('src', 'http://fedoraproject.org/maps/' + release + '/' + release + '.x86_64.png'));
            $('#maps').append($('<img/>').attr('src', 'http://fedoraproject.org/maps/' + release + '/' + release + '.ppc.png').load(function() { setTimeout(function(){ $('#maps').imagefit(); }, 100); }));
        }

    """}

class UserMapsWidget(Widget):
    children = [ReleaseDownloadsFilter('releases')]
    javascript = [jquery_imagefit_js]
    template = """
        ${c.releases(options=releases, value='all')}
        <br/>
        <div id="maps">
            <img src="http://fedoraproject.org/maps/all.png"/>
        </div>
        <script>
            $(document).ready(function(){
                setTimeout(function(){ 
                    $('#maps').imagefit();
                }, 100);
            });
        </script>
    """
    engine_name = 'mako'

    def update_params(self, d):
        super(UserMapsWidget, self).update_params(d)
        pkgdb = get_connector('pkgdb')
        releases = []
        for release in pkgdb.get_fedora_releases():
            rel = release[0].replace('dist-', '')
            if 'epel' in rel:
                rel = 'el' + rel[0]
            releases.append((rel, release[1]))
        d.releases = releases + [('all', 'All releases')]

user_maps_widget = UserMapsWidget('user_maps')


class UserStatisticsDashboard(DashboardContainer):
    layout = [
            Category('left-content-column-apps', [
                MokshaWidget('User Maps', user_maps_widget),
                ]),
    ]

user_stats_dashboard = UserStatisticsDashboard('user_stats')
