from moksha.lib.base import Controller
from tg import expose, tmpl_context, override_template, request, url
from fedoracommunity.widgets import LoginWidget
from urlparse import urlparse

login_widget = LoginWidget('login_widget')

class RootController(Controller):

    @expose()
    def index(self, view='home', came_from=None):
        tmpl_context.widget = login_widget

        if (view == 'canvas'):
            override_template(self.index, 'mako:fedoracommunity.mokshaapps.login.templates.index_canvas')
        else: # view = home
            override_template(self.index, 'mako:fedoracommunity.mokshaapps.login.templates.index')


        if not came_from:
            came_from = url('/')
        else:
            # only redirect to relative addresses to avoid phishing
            purl = urlparse(came_from)
            came_from = purl.path
            if purl.query:
                came_from += '?' + purl.query

        return {'came_from': came_from}