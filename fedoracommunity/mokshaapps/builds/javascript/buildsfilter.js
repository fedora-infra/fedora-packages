// This file is part of Fedora Community.
// Copyright (C) 2008-2009  Red Hat, Inc.
// 
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU Affero General Public License as
// published by the Free Software Foundation, either version 3 of the
// License, or (at your option) any later version.
// 
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU Affero General Public License for more details.
// 
// You should have received a copy of the GNU Affero General Public License
// along with this program.  If not, see <http://www.gnu.org/licenses/>.

function _builds_filter_selected(o, d) {
  data = $(d.element).data('.moksha_selectable_data');
  if (data.show_secondary_tables) {
    $('.secondary_table').fadeIn();
  } else {
    $('.secondary_table').fadeOut();
  }

  var main_table = $('.main_table');
  $('h3', main_table).html(data.label);
  $('table', main_table).mokshagrid("request_update", data);
}