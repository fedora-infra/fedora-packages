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
