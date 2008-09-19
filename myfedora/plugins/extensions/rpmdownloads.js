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
        var more_link = $("<a/>");
        more_link.attr("href","javascript:void(0);");

        more_link.text("more");
        dl_item.append(more_link);
        dl_item.append("]");

        /* guess the user's arch and only display those files
           unless expanded with the more link */
        var arch = myfedora.guess_client_arch('i386'); 

        var devel_file_match = /.*-(devel|doc|debuginfo|src)-.*/;
        var has_arch_files = false;
        var more_view = jQuery('<div />').attr("id", hidden_class_name);
       
        /* loop over primary arch */
        for (var i in arch) {
          var a = arch[i];
          arch_files = downloads[a];
          var more_arch_block = $("<div />");
          
          if (arch_files) {
            more_arch_block.append($("<h3 />").text(a));
            has_arch_files = true;
            var arch_list = $("<ul />");
            var more_arch_list = $("<ul />");
            var more_arch_item;
            more_arch_block.append(more_arch_list);
  
            for (i in arch_files) {
              var f = arch_files[i];

              more_arch_item = $("<li/>");
              dl_link = $("<a/>").attr("href", f.url).append(f.name);
              more_arch_item.append(dl_link);
              more_arch_list.append(more_arch_item);
              
              // don't display devel files
              if (f.name.match(devel_file_match))
                continue;

              arch_item = $("<li/>");

              dl_link = $("<a/>").attr("href", f.url).append(f.name);
              arch_item.append(dl_link);
              arch_list.append(arch_item);
            }
            
            more_view.append(more_arch_block);
            
            dl_item.append(arch_list);
            delete downloads[a];

            /* only get the first arch with files 
             * since it should be the best match
             */
            break;
          }
        }

        /* loop over the downloads and add them to the display */
        for (var a in downloads) {
          if (a == 'count') {
            continue;  
          }
          
          var arch_list = $('<div />');
          var arch_files = downloads[a];
          if (arch_files) {
            var arch_li = $("<h3 />").append(a);
            arch_list.append(arch_li);
            var arch_ul = $("<ul />");
            for (i in arch_files) {
              var f = arch_files[i];

              arch_item = $("<li/>");

              var dl_link = $("<a/>").attr("href", f.url).append(f.name);
              arch_item.append(dl_link);
              arch_ul.append(arch_item);
            }

            arch_list.append(arch_ul);
            
            more_arch_block.append(arch_list);
          }
          
        }

        /* only show the downloads links if no arch files are available */
        if (!has_arch_files)
          {
             more_link.text("Downloads");
             dl_item.html(more_link);
          }
          
        block.html(dl_item.contents())
        block.append(more_view);
        var lb = new myfedora.ui.lightbox(more_view, 5);
        console.log(lb);
          
        more_link.click(function() {
                          lb.show();  
                        });
      }
      
    /* get the tags to process */
    var burl = myfedora.get_page_base_url();
    params = {'task_id' : data.task_id,
              'state': data.build_state}
    jQuery.getJSON(burl + 'proxy/koji/get_files',
                   params,
                   render);
    
    return "RPM list " + myfedora.loading();
  }
}
