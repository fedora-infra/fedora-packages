from route import Route

class BuildsRoute(Route):
    def __init__(self):
        Route.__init__(self, "myfedora.templates.packages.builds")

    def default(self, dict, package, *args, **kw):
        dict['tg_template'] = self.get_default_template()

        return dict
