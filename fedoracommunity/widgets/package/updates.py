from moksha.api.widgets import Grid

class ActiveReleasesGrid(Grid):
    template='mako:fedoracommunity.widgets.package.templates.active_releases'
    params=['package_name']
    resource = 'bodhi'
    resource_path = 'query_active_releases'

    def update_params(self, d):
        d['filters'] = {'package': d['package_name']}
        d['rows_per_page'] = 10
        super(ActiveReleasesGrid, self).update_params(d)

active_releases_widget = ActiveReleasesGrid('active_release_grid')
