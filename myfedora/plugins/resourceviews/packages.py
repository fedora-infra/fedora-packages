from myfedora.lib.app_factory import ResourceViewAppFactory

from tw.jquery import jquery_js, jQuery
from tw.api import Widget, JSLink, js_function, js_callback

import pylons

class PackagesViewApp(ResourceViewAppFactory):
    entry_name = 'packages'
