# This file is part of Fedora Community.
# Copyright (C) 2008-2009  Red Hat, Inc.
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

from moksha.api.widgets import Selectable

class QuickLinksWidget(Selectable):
    links = [('My Profile',
              'View my profile',
              '/my_profile',
              'view_profile'),
             ('Package Maintenance',
              'View my packages',
              '/my_profile/package_maintenance',
              'view_my_packages'),
             ('Package Maintenance',
              'View my builds',
              '/my_profile/package_maintenance/builds_overview',
              'view_my_builds'),
             ('Package Maintenance',
              'View my pending updates',
              '/my_profile/package_maintenance/unpushed_updates',
              'view_my_pending_updates'),
             ('Search',
              'Search for packages',
              '/search/?st=packages',
              'search_packages'),
              ('Search',
              'Search for people',
              '/search/?st=people',
              'search_people')]
    @staticmethod

    def add_link(d, category, label, link, content_id):
        cats = d.get('categories')
        if not cats:
            cats = []

        category_match = None
        for c in cats:
            if category == c['label']:
                category_match = c
                break

        if not category_match:
            category_match = {'label': category, 'items':[]}
            cats.append(category_match)

        category_match['items'].append({'label': label,
                                        'link': link,
                                        'content_id': content_id})

        d['categories'] = cats


    def update_params(self, d):
        # standard quick link items
        for link in self.links:
            self.add_link(d, *link)

        super(QuickLinksWidget, self).update_params(d)
