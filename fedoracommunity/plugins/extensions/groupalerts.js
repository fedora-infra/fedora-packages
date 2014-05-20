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
    consumes:['alerts_groups'],
    author: 'John (J5) Palmieri <johnp@redhat.com>',
    version: '0.1',
    name: 'Group Alerts',
    summary: 'Displays users who have requested group access',
    description: 'Displays users who have requested group access \
                  that you have rights to \
                  \
                  Required Extension Point Data: \
                  \
                  \ None, you must be logged in though'
  },

  run: function (data) {
    var burl = moksha.get_page_base_url();
    var PROXY_URL = burl + 'proxy/fas/get_todo_list_page';
    var FAS_URL = '//admin.fedoraproject.org/accounts/';
    var self = this;
    var hidden_parent = undefined;

    if (data.hide_parent)
      hidden_parent = jQuery('#' + data.hide_parent);

    render = function(html)
      {
        var div = jQuery("#" + data.uid);
        var ul = jQuery(".queue", html);

        var links = jQuery("a", ul);
        for (var i=0; i < links.length; i++)
          {
            // for now rewrite to bring you to fas
            var l = jQuery(links[i]);
            l.attr('target', '_blank');
            var href = l.attr('href');
            l.attr('href', FAS_URL + href);
          }

        if(ul.length > 0)
          {
            div.append(ul);
            if (hidden_parent)
              hidden_parent.show();
          }

      }

    jQuery.get(PROXY_URL,
               render,
               "html");

  }
 }

