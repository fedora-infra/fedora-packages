
import tw2.core as twc
from moksha.wsgi.widgets.moksha_js import moksha_js

fcomm_js = twc.JSLink(
    modname=__name__,
    filename="static/js/fcomm.js",
    resources=[moksha_js],
)

