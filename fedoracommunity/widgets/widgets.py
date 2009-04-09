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

from tw.api import Widget, JSLink, CSSLink
from tw.jquery import jquery_js

# FIXME: myfedora js code should go into moksha and be eliminated
jquery_template_js = JSLink(modname='moksha', filename='public/javascript/jquery.template.js', javascript=[jquery_js])
jquery_json_js = JSLink(modname='moksha', filename='public/javascript/jquery.json.js', javascript=[jquery_js])

fedora_css = CSSLink(link='https://fedoraproject.org/static/css/fedora.css')
fedoracommunity_appchrome_css = CSSLink(modname='fedoracommunity', filename='public/css/application-chrome.css')
fedoracommunity_branding_css = CSSLink(modname='fedoracommunity', filename='public/css/myfedora-branding.css')

class PagerWidget(Widget):
    template = "mako:/myfedora/widgets/templates/pager.html"
    params = ['page', 'last_page', 'show', 'parent_dom_id']
    show = 7
    page = 1

    def update_params(self, d):
        super(PagerWidget, self).update_params(d)

        page = int(d['page'])
        if page < 1:
            page = 1

        last_page = int(d['last_page'])

        # how many of the main set do we show
        show = int(d['show'])

        parent_id = d['parent_dom_id']

        front_set = []
        back_set = []
        main_set = []

        max_block_num = last_page / show

        # figure out main set
        block_num = page / show

        start = block_num * show + 1
        last_in_set = start + show
        if last_in_set >= last_page:
            start = last_page - show + 1
            if start < 1:
                start = 1;

            last_in_set = last_page + 1
            block_num = max_block_num

        main_set = range(start, last_in_set)

        # do we need a front set
        if block_num > 0:
            front_set = [1]

        # do we need a back set
        if block_num < max_block_num:
            back_set = [last_page]

        prev_page = None
        if page > 1:
            prev_page = page - 1

        next_page = None
        if page < last_page:
            next_page = page + 1

        d.update({'front_set': front_set,
                  'back_set': back_set,
                  'main_set': main_set,
                  'prev_page': prev_page,
                  'next_page': next_page,
                  'parent_id': parent_id,
                  'page': page,
                  'last_page': page,
                  'show': show})

