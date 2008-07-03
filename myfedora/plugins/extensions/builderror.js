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
    
    render = function(json) 
      {
        log_url = json.log_url;
        log_name = json.log_name;

        msg_div = jQuery("<div />");
        msg_div.append("Error in build.");
        if (log_url) {
          link = $("<a/>").attr("href", log_url).attr("target", "_blank");
          link.append("You can refer to log ");
          link.append(log_name);
          link.append(" for more details");
          msg_div.append(link);
        } else {
          msg_div.append(" No logs are available to inspect");
        }

        msg_div.hide(); 
        jQuery("#" + data.uid).html(msg_div);
        msg_div.fadeIn("slow");
      }
      
    params = {'task_id' : data.task_id}
    jQuery.getJSON('http://localhost:8080/proxy/koji/get_error_log',
                   params,
                   render);
                   
    jQuery("#" + data.uid).css('background-color', '#ffcccc');
    return('Attempting to load error log for failed build...'); 
  }
 }
 