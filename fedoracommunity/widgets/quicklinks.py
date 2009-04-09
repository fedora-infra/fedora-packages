from moksha.api.widgets import Selectable

class QuickLinksWidget(Selectable):
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
        self.add_link(d, 'My Profile',
                         'View my profile',
                         '/profile',
                         'view_profile')
        self.add_link(d, 'Package Maintenance',
                         'View my packages',
                         '/my_profile/packages_maintenance',
                         'view_my_packages')
        self.add_link(d, 'Package Maintenance',
                         'View my builds',
                         '/package_maintenance/builds/my_overview',
                         'view_my_builds')
        self.add_link(d, 'Package Maintenance',
                         'View my pending updates',
                         '/package_maintenance/updates/my_unpushed',
                         'view_my_pending_updates')

        super(QuickLinksWidget, self).update_params(d)
