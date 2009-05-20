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
    consumes:['build_menu'],
    author: 'John (J5) Palmieri <johnp@redhat.com>',
    version: '0.2',
    name: 'Build Changelog Message',
    summary: 'Displays a link to get the latest changelog for this build',
    description: 'Displays a link that when focused will show the latest \
                  changelog for the task_id \
                  Required Extension Point Data: \
                  \
                  - build_id: The build id of the build \
                  - task_id: The task id of the build just incase we need to \
                             lookup the srpm \
                  - build_state: The state the build is in \
                  - menu_id: The id of the menu we are attaching to \
                  '
  },
  run: function (data) {
    var render = function(json)
      {
          var $changelog_container = $('#' + data.uid);
          $changelog_container.append(json.date + ' ' + json.author + '<br/>');
          var v= json.text.split('\n');
          for (i in v) {
              line = v[i];

              $changelog_container.append(line + "<br/>");
          }
      }

    var $menu = $('#' + data.menu_id)
    var on_show_load_changelog = function() {
        var params = {'build_id': data.build_id,
                      'task_id': data.task_id,
                      'state': data.build_state}

        $menu.unbind('show.changelog');

        moksha.connector_load('koji', 'get_latest_changelog',
                   params,
                   render,
                   data.overlay,
                   moksha.url('/images/spinner-20.gif')
                   );
    }

    $menu.bind('show.changelog', on_show_load_changelog);

    return('');
  }
 }
