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

from moksha.lib.helpers import CategoryEnum

updates_links = CategoryEnum('updates_links',
                             ('PACKAGE',
                              '/package_maintenance/packages/package/updates'
                             ),
                             ('ALL_UPDATES',
                              '/package_maintenance/updates'
                             ),
                             ('STABLE_UPDATES',
                              '/package_maintenance/updates/stable_updates'
                             ),
                             ('TESTING_UPDATES',
                              '/package_maintenance/updates/testing_updates'
                             ),
                             ('UNPUSHED_UPDATES',
                              '/package_maintenance/updates/unpushed_updates'
                             )
                           )
