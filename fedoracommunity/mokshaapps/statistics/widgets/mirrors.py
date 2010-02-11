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

from tw.api import Widget
from moksha.api.widgets.containers import DashboardContainer
from moksha.lib.helpers import Category, Widget as MokshaWidget

class MirrorManagerMapsWidget(Widget):
    template = '<img src="http://fedoraproject.org/maps/mirrors.png"/>'

mirrormanager_maps_widget = MirrorManagerMapsWidget('mirror_maps')

class MirrorStatisticsDashboard(DashboardContainer):
    layout = [
            Category('left-content-column-apps', [
                MokshaWidget('Fedora Mirrors', mirrormanager_maps_widget),
                ]),
    ]

mirror_stats_dashboard = MirrorStatisticsDashboard('mirror_stats')
