from tw.api import Widget
from tg import url
from pylons import request

class LoginWidget(Widget):
    params=['username', 'password']
    template = 'mako:fedoracommunity.widgets.templates.login'

    def update_params(self, d):
        super(LoginWidget, self).update_params(d)
