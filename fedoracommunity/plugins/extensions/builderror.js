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
    consumes:['build_message'],
    author: 'John (J5) Palmieri <johnp@redhat.com>',
    version: '0.1',
    name: 'Build Error Message',
    summary: 'Displays an error message and links to the log if the build failed',
    description: 'If the build fails this extension attempts to figure out      \
                  which log has the error in it and displays a link to the log. \
                  \
                  Required Extension Point Data: \
                  \
                  - task_id: The task id of the build \
                  - build_state: The status of the build \
                  '
  },

  BUILD_STATE_FAILED: 3,

  run: function (data) {
    if (data.build_state != this.BUILD_STATE_FAILED)
      {
        return;
      }

    var render = function(json)
      {
        log_url = json.log_url;
        log_name = json.log_name;

        msg_div = jQuery("<span />").addClass('error_message');
        msg_div.append("Error in build.");
        if (log_url) {

          msg_div.append("You can refer to log ");
          link = $("<a/>").attr("href", log_url).attr("target", "_blank");
          link.append(log_name);
          msg_div.append(link);
          msg_div.append(" for more details");
        } else {
          msg_div.append(" No logs are available to inspect");
        }

        msg_div.hide();
        var $uid = jQuery("#" + data.uid)
        $uid.html(msg_div);
        msg_div.fadeIn("slow");
      }

    var params = {'task_id' : data.task_id}
    var burl = moksha.get_base_url();

    fcomm.connector_load('koji', 'get_error_log',
                   params,
                   render,
                   data.overlay,
                   moksha.url('/images/spinner-20.gif')
                   );

    return('Attempting to load error log for failed build...');
  }
 }
