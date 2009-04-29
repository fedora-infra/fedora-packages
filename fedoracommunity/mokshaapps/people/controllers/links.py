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

_base_links = [('MEMBERSHIPS','memberships')]

def construct_link_tuple_from_list(prefix, base_links):
    full_links = []
    for (id, link) in base_links:
        full_links.append((id, prefix + '/' + link))

    return full_links

user_links = construct_link_tuple_from_list('/people', _base_links)
profile_links = construct_link_tuple_from_list('/my_profile', _base_links)

membership_links = CategoryEnum('membership_link',
                                 *user_links
                               )
profile_membership_links = CategoryEnum('membership_link',
                                        *profile_links
                               )
