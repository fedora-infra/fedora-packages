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

from moksha.lib.helpers import CategoryEnum, EnumGroup

builds_links = CategoryEnum('build_link',
                             ('PACKAGE',
                              '/package_maintenance/packages/package/builds'
                             ),
                             ('ALL_BUILDS',
                              '/package_maintenance/builds'
                             ),
                             ('IN_PROGRESS',
                              '/package_maintenance/builds/inprogress',
                             ),

                             ('FAILED',
                              '/package_maintenance/builds/failed',
                             ),

                             ('SUCCESSFUL',
                              '/package_maintenance/builds/successful',
                             ),
                           )

my_builds_links = CategoryEnum('my_build_link',
                             ('PACKAGE',
                              '/package_maintenance/packages/package/my_builds'
                             ),
                             ('ALL_BUILDS',
                              '/package_maintenance/my_builds'
                             ),
                             ('IN_PROGRESS',
                              '/package_maintenance/builds/my_inprogress',
                             ),

                             ('FAILED',
                              '/package_maintenance/builds/my_failed',
                             ),

                             ('SUCCESSFUL',
                              '/package_maintenance/builds/my_successful',
                             ),
                           )

profile_builds_links = CategoryEnum('profile_build_link',
                             ('ALL_BUILDS',
                              '/my_profile/package_maintenance/builds_overview'
                             ),
                             ('IN_PROGRESS',
                              '/my_profile/package_maintenance/builds_inprogress',
                             ),

                             ('FAILED',
                              '/my_profile/package_maintenance/builds_failed',
                             ),

                             ('SUCCESSFUL',
                              '/my_profile/package_maintenance/builds_successful',
                             ),
                           )

people_builds_links = CategoryEnum('people_build_link',
                             ('ALL_BUILDS',
                              '/people/package_maintenance/builds_overview'
                             ),
                             ('IN_PROGRESS',
                              '/people/package_maintenance/builds_inprogress',
                             ),

                             ('FAILED',
                              '/people/package_maintenance/builds_failed',
                             ),

                             ('SUCCESSFUL',
                              '/people/package_maintenance/builds_successful',
                             ),
                           )

builds_links_group = EnumGroup()
builds_links_group.add(builds_links)
builds_links_group.add(my_builds_links)
builds_links_group.add(profile_builds_links)
builds_links_group.add(people_builds_links)
