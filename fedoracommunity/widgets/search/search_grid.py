from fedoracommunity.widgets.grid import Grid

class XapianSearchGrid(Grid):
    template="mako:fedoracommunity.widgets.search.templates.search_results"
    resource = 'xapian'
    resource_path = 'search_packages'
    morePager = True
    onReady = "ready_search()"
