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
Fedora Updates Statistics Widgets
=================================

.. moduleauthor:: Luke Macken <lmacken@redhat.com>
"""

from tw.forms import SingleSelectField
from fedoracommunity.widgets.flot import FlotWidget

class ReleaseDownloadsFilter(SingleSelectField):
    options = []
    attrs = {'onchange': """\
        moksha.html_load(moksha.url('/apps/fedoracommunity.statistics/updates'), {
            'release': $('#releases').val()
        }, function(r) {
            var $stripped = moksha.filter_resources(r);
            $('.left-content-column').html($stripped);
        });
    """}

release_downloads_filter = ReleaseDownloadsFilter('releases')


class AllUpdatesWidget(FlotWidget):
    params = ['release', 'release_name', 'data']

    def update_params(self, d):
        release = d['release']
        release_name = d['release_name']
        data = d['data'][release]['AllMetric']
        d.data = [
            {
                'data'  : data['all'],
                'label' : 'All Updates',
                'bars'  : {'show': 'true'}
            },
            {
                'data'   : data['timeline']['enhancement'],
                'label'  : 'Enhancement',
                'lines'  : {'show': 'true'},
                'points' : {'show': 'true'}
            },
            {
                'data'   : data['timeline']['security'],
                'label'  : 'Security',
                'lines'  : {'show': 'true'},
                'points' : {'show': 'true'}
            },
            {
                'data'   : data['timeline']['bugfix'],
                'label'  : 'Bugfix',
                'lines'  : {'show': 'true'},
                'points' : {'show': 'true'}
            }]
        d.options = {
                'xaxis' : {'ticks': data['months']},
            }
        d.label = '%s Updates' % release_name
        d.width = '500px'
        super(AllUpdatesWidget, self).update_params(d)


all_updates_widget = AllUpdatesWidget('all_updates_widget')
