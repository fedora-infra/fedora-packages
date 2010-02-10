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
MirrorManager map viewing widget
================================

.. moduleauthor:: Luke Macken <lmacken@redhat.com>
"""

from pylons import cache
from fedora.client import Wiki
from tw.api import Widget
from tw.forms import SingleSelectField
from datetime import datetime, timedelta
from moksha.api.widgets import Grid
from moksha.api.widgets.containers import DashboardContainer
from moksha.lib.helpers import Category, Widget as MokshaWidget, defaultdict
from moksha.api.connectors import get_connector
from fedoracommunity.widgets.flot import FlotWidget
import simplejson

class ReleaseDownloadsFilter(SingleSelectField):
    options = []
    attrs = {'onchange': """
        var release = $('#mirror_maps_releases').val();
        $('#maps').empty();
        if (release == 'all') {
            $('#maps').append($('<img/>').attr('src', 'http://fedoraproject.org/maps/all.png'));
        } else {
            $('#maps').append($('<img/>').attr('src', 'http://fedoraproject.org/maps/' + release + '/' + release + '.i386.png'));
            $('#maps').append($('<img/>').attr('src', 'http://fedoraproject.org/maps/' + release + '/' + release + '.x86_64.png'));
            $('#maps').append($('<img/>').attr('src', 'http://fedoraproject.org/maps/' + release + '/' + release + '.ppc.png'));
        }
    """}

class MirrorManagerMapsWidget(Widget):
    children = [ReleaseDownloadsFilter('releases')]
    template = """
        ${c.releases(options=releases, value='all')}
        <br/>
        <div id="maps">
            <img src="http://fedoraproject.org/maps/all.png"/>
        </div>
    """
    engine_name = 'mako'

    def update_params(self, d):
        super(MirrorManagerMapsWidget, self).update_params(d)
        pkgdb = get_connector('pkgdb')
        releases = []
        for release in pkgdb.get_fedora_releases():
            rel = release[0].replace('dist-', '')
            if 'epel' in rel:
                rel = 'el' + rel[0]
            releases.append((rel, release[1]))
        d.releases = releases + [('all', 'All releases')]

mirrormanager_maps_widget = MirrorManagerMapsWidget('mirror_maps')


class MirrorStatisticsDashboard(DashboardContainer):
    layout = [
            Category('left-content-column-apps', [
                MokshaWidget('MirrorManager Maps', mirrormanager_maps_widget),
                ]),
    ]

mirror_stats_dashboard = MirrorStatisticsDashboard('mirror_stats')
