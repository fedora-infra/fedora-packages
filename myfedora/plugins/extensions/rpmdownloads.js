{  
  info: {
    consumes:['build_details'],
    author: 'John (J5) Palmieri <johnp@redhat.com>',
    version: '0.1',
    name: 'RPM Downloads',
    summary: 'Display downloadable files for a build',
    description: 'Displays all available RPMS for a given build     \
                  \
                  Required Extension Point Data: \
                  \
                  - task_id: the id of the build task so we get a list of RPMS \
                  - build_state: the state the build is in \
                  '
  },
  
  run: function (data) {
    /************* Renders the releases into HTML ***************/                    
    render = function(json) 
      {
        var block = jQuery('#' + data.uid);
        var hidden_class_name = "more_" + data.uid;
        var dl_item = $("<span/>").text("Dowloads");
        var downloads = json.files.downloads; 
        /* no use dealing with downloads if there are non so remove
           download div and return */
           
        if (!downloads || !downloads.count)
          {
            block.remove();
            return;
          }
 
        /* show and hide all files */
        dl_item.append("[");
        var more_link = $("<a/>").attr("id", hidden_class_name);
        more_link.attr("href","javascript:void(0);");

        more_link.click(function() {
                          _render_files_tags_more_or_less(downloads); 
                        });

        more_link.text("more");
        dl_item.append(more_link);
        dl_item.append("]");

        /* guess the user's arch and only display those files
           unless expanded with the more link */
        var arch = myfedora.guess_client_arch('i386'); 

        var devel_file_match = /.*-(devel|doc|debuginfo|src)-.*/;
        var has_arch_files = false;
        
        /* loop over primary arch */
        for (i in arch) {
          var a = arch[i];
          arch_files = downloads[a];
          
          if (arch_files) {
            has_arch_files = true;
            var arch_list = $("<ul />");
 
            for (i in arch_files) {
              var f = arch_files[i];

              // don't display devel files
              if (f.name.match(devel_file_match))
                continue;

              arch_item = $("<li/>");

              dl_link = $("<a/>").attr("href", f.url).append(f.name);
              arch_item.append(dl_link);
              arch_list.append(arch_item);
            }

            dl_item.append(arch_list);
            delete downloads[a];

            /* only get the first arch with files 
             * since it should be the best match
             */
            break;
          }
        }

        /* only show the downloads links if no arch files are available */
        if (!has_arch_files)
          {
             more_link.text("Downloads");
             dl_item.html(more_link);
          }
          
        block.html(dl_item.contents());
      }
      
    /* get the tags to process */
    params = {'task_id' : data.task_id,
              'state': data.build_state}
    jQuery.getJSON('http://localhost:8080/proxy/koji/get_files',
                   params,
                   render);
    
    return "RPM list " + myfedora.loading();
  }
}
