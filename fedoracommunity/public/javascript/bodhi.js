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

function update_action(update, action) {
    args = {}
    args['update'] = update;
    args['action'] = action;

    if (typeof(moksha_csrf_token)!='undefined' && moksha_csrf_token) {
        args['_csrf_token'] = moksha_csrf_token;
    }

    $.getJSON('/moksha_connector/bodhi/request_data/request', args, function(json) {
        json = json[1];
        $('#flash').text('');
        $('div.left-content-column').prepend($('<span/>').attr('id', 'flash').text(json.tg_flash)).show('slow');
        if (typeof(json.update) != 'undefined' && json.update.request == action) {
            $('#' + update.replace(/\./g, '') + '_' + action).hide('slow');
        }
    });

}
