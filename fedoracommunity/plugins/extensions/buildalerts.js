{
  info: {
    consumes:['alerts_packages'],
    author: 'John (J5) Palmieri <johnp@redhat.com>',
    version: '0.1',
    name: 'Build Alerts',
    summary: 'Displays recent build information',
    description: 'A user is usually concerned with recent builds.     \
                  This extension will show the status of recent builds \
                  within the day and stats on builds within the week. \
                  \
                  Required Extension Point Data: \
                  \
                  - user: The username of the person we are looking up builds for \
                  - base_url: URL to the user\'s resource view'
  },

  BUILD_STATE_FAILED: 3,
  BUILD_STATE_COMPLETE: 1,
  BUILD_STATE_BUILDING: 0,
  IMG_STATE_FAILED: '/images/16_failure_build.png',
  IMG_STATE_COMPLETE: '/images/16_success_build.png',
  IMG_STATE_BUILDING: 'http://koji.fedoraproject.org/koji-static/images/building.png',

  run: function (data) {
    var burl = moksha.get_base_url();
    var buildsurl = data.base_url + 'builds/';
    var self = this;
    var hidden_parent = undefined;

    if (data.hide_parent)
      hidden_parent = jQuery('#' + data.hide_parent);

    render = function(json)
      {
        var builds = json.builds

        var div = jQuery("#" + data.uid);
        var num_failed_builds = 0;
        var num_complete_builds = 0;

        for (var i in builds) {
          var build  = builds[i];
          var d = new Date();
          var now = d.getTime()/1000;

          var name = build.name;
          var nvr = build.nvr;
          var state = build.state;
          var ctime = build.completion_time;
          var stime = build.creation_time;

          // if completed > a day ago, hold off and enter it as part of
          // alert statistics for the week
          var day_in_seconds = 86400;
          var elapsed_time = now - ctime;
          var is_today = elapsed_time < day_in_seconds;

          var elapsed_minutes = 0;
          var elapsed_hours = 0;
          var elapsed_str = '';
          if (is_today)
            {
               elapsed_minutes = parseInt(elapsed_time / 60);
               elapsed_hours = parseInt(elapsed_minutes / 60);

               if (elapsed_hours >= 1)
                 {
                   if (elapsed_hours == 1)
                     {
                       elapsed_hours + " hour ago";
                     }
                   else
                     {
                       elapsed_str = elapsed_hours + " hours ago";
                     }
                 }
               else
                 {
                   elapsed_str = elapsed_minutes + " minutes ago";
                 }
            }

          var alert = jQuery('<div />');

          if (state == self.BUILD_STATE_BUILDING)
            {
              alert.append(jQuery("<img />").attr('src', self.IMG_STATE_BUILDING));
              alert.append(name + " has been building since " + stime);
            }
          else if (state == self.BUILD_STATE_FAILED)
            {
              if (!is_today)
                {
                  num_failed_builds++;
                  continue;
                }
              alert.append(jQuery("<img />").attr('src', self.IMG_STATE_FAILED));

              alert.append(jQuery('<a>' + name + " failed " + elapsed_str + '</a>').attr('href', buildsurl + '?package=name'));
            }
          else if (state == self.BUILD_STATE_COMPLETE)
            {
              if (!is_today)
                {
                  num_complete_builds++;
                  continue;
                }
              alert.append(jQuery("<img />").attr('src', self.IMG_STATE_COMPLETE));
              alert.append(jQuery('<a>' + name + " built " + elapsed_str+ '</a>').attr('href', buildsurl + '?package=name'));
            }
          else
            {
              continue;
            }

          div.append(alert);
          if (hidden_parent)
            hidden_parent.show();
        }

        if (num_failed_builds > 0)
          {
            var plural = 's';
            if (num_failed_builds == 1)
              plural = '';
            var alert = jQuery('<div />');
            alert.append(jQuery("<img />").attr('src', self.IMG_STATE_FAILED));

            var a = jQuery('<a />').attr('href', buildsurl + '?filter_failed=true');
            a.append(num_failed_builds + ' recent failed build' + plural);
            alert.append(a);
            div.append(alert);
            if (hidden_parent)
              hidden_parent.show();
          }

        if (num_complete_builds > 0)
          {
            var plural = 's';
            if (num_complete_builds == 1)
              plural = '';
            var alert = jQuery('<div />');
            alert.append(jQuery("<img />").attr('src', self.IMG_STATE_COMPLETE));
            var a = jQuery('<a/>').attr('href', buildsurl + '?filter_successful=true');
            a.append(num_complete_builds + ' recent successful build' + plural);
            alert.append(a);
            div.append(alert);
            if (hidden_parent)
              hidden_parent.show();
          }
      }

    var complete_url = burl + 'proxy/koji/list_builds';
    // get all non-complete builds
    var params = {'user' : data.user,
                  'state': self.BUILD_STATE_BUILDING,
                  'epoch': true,
                  'order': '-creation_time'};
    jQuery.getJSON(complete_url,
                   params,
                   render);

    // get all completed builds this week
    var d = new Date();
    var now = parseInt(d.getTime()/1000);
    var one_week_ago = now - 604800; // number of seconds in a week
    var params = {'user' : data.user,
                  'complete_after': one_week_ago,
                  'epoch': true,
                  'order': '-completion_time'
                  };


    jQuery.getJSON(complete_url,
                   params,
                   render);
  }
 }
