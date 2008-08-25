# Copyright (C) 2008  Red Hat, Inc. All rights reserved.
#
# This copyrighted material is made available to anyone wishing to use, modify,
# copy, or redistribute it subject to the terms and conditions of the GNU
# General Public License v.2.  This program is distributed in the hope that it
# will be useful, but WITHOUT ANY WARRANTY expressed or implied, including the
# implied warranties of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.  You should have
# received a copy of the GNU General Public License along with this program; if
# not, write to the Free Software Foundation, Inc., 51 Franklin Street, Fifth
# Floor, Boston, MA 02110-1301, USA. Any Red Hat trademarks that are
# incorporated in the source code or documentation are not subject to the GNU
# General Public License and may only be used or replicated with the express
# permission of Red Hat, Inc.
#
# Author(s): Luke Macken <lmacken@redhat.com>

from tg import url
from tw.api import Widget, JSLink, CSSLink, js_function, js_callback
from tw.jquery import jquery_js, jQuery

myfedora_js = JSLink(link='/javascript/myfedora.js')
myfedora_ui_js = JSLink(link='/javascript/myfedora.ui.js')
myfedora_extentions_js = JSLink(link='/javascript/myfedora.extensions.js')

fedora_css = CSSLink(link='http://fedoraproject.org/static/css/fedora.css')
myfedora_table_css = CSSLink(link='/css/myfedora-style-tables.css')
myfedora_appchrome_css = CSSLink(link='/css/application-chrome.css')
myfedora_branding_css = CSSLink(link='/css/myfedora-branding.css')

class GlobalResourceInjectionWidget(Widget):
    javascript=[myfedora_js]
    css=[fedora_css, 
         myfedora_table_css, 
         myfedora_appchrome_css, 
         myfedora_branding_css]