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

import tw2.core as twc
from tw2.core.params import Param
from tg.controllers import url

class CSSLink(twc.CSSLink):
    path = Param('Path to where you would find these files on the web server')
    def prepare(self):
        self.link = url(self.path)
        super(CSSLink, self).prepare()

fedora_css = CSSLink(modname='fedoracommunity', path='/css/fedora.css')
fedoracommunity_appchrome_css = CSSLink(modname='fedoracommunity', path='/css/application-chrome.css')
fedoracommunity_branding_css = CSSLink(modname='fedoracommunity', path='/css/myfedora-branding.css')
fedoracommunity_reset_css = CSSLink(modname='fedoracommunity', path='/css/reset.css')
fedoracommunity_text_css = CSSLink(modname='fedoracommunity', path='/css/text.css')
fedoracommunity_960_24_col_css = CSSLink(modname='fedoracommunity', path='/css/960_24_col.css')


class PagerWidget(twc.Widget):
    template = "mako:/myfedora/widgets/templates/pager.html"
    page = twc.Param('The page to view', default=1)
    last_page = twc.Param()
    show = twc.Param('The number of items to show', default=7)
    parent_dom_id = twc.Param()

    front_set = twc.Variable()
    back_set = twc.Variable()
    main_set = twc.Variable()
    prev_page = twc.Variable()
    next_page = twc.Variable()
    parent_id = twc.Variable()

    def prepare(self):
        super(PagerWidget, self).prepare()

        self.page = int(self.page)
        if self.page < 1:
            self.page = 1

        self.last_page = int(self.last_page)

        # how many of the main set do we show
        self.show = int(self.show)

        self.parent_id = self.parent_dom_id

        self.front_set = []
        self.back_set = []
        self.main_set = []

        max_block_num = self.last_page / self.show

        # figure out main set
        block_num = self.page / self.show

        start = block_num * self.show + 1
        last_in_set = start + self.show
        if last_in_set >= self.last_page:
            start = self.last_page - self.show + 1
            if start < 1:
                start = 1

            last_in_set = self.last_page + 1
            block_num = max_block_num

        self.main_set = range(start, last_in_set)

        # do we need a front set
        if block_num > 0:
            self.front_set = [1]

        # do we need a back set
        if block_num < max_block_num:
            self.back_set = [self.last_page]

        self.prev_page = None
        if self.page > 1:
            self.prev_page = self.page - 1

        self.next_page = None
        if self.page < self.last_page:
            self.next_page = self.page + 1
