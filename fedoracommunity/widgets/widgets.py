# This file is part of Fedora Community.
# Copyright (C) 2008-2010  Red Hat, Inc.
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
# 
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from tw.api import Widget, JSLink, CSSLink
from tw.jquery import jquery_js
from moksha.widgets.jquery_template import jquery_template_js

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
                start = 1

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

