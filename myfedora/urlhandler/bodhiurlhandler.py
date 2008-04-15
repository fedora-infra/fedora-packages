from urlhandler import URLHandler

class BodhiURLHandler(URLHandler):
    def __init__(self):
        URLHandler.__init__(self)

        self.set_base_url('https://admin.fedoraproject.org/updates')
        self._set_link_type(self.INTERNAL_LINK)
        self.route = None

    def get_route(self):
        if not self.route:
            from myfedora.packagecontroller.updatesroute import UpdatesRoute
            self.route = UpdatesRoute()

        return self.route

