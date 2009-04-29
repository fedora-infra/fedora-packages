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

{
  info: {
    consumes:['make_menu'],
    author: 'John (J5) Palmieri <johnp@redhat.com>',
    version: '0.1',
    name: 'Menu Creator',
    summary: 'Async creation of menus used inside of templates',
    description: 'Since jQuery templates can\'t have javascript in \
                  them we use this to create a javascript menu'
  },

  run: function (data) {
    $('#' + data.placeholder_id).moksha_popup();

    return null;
  }
 }
