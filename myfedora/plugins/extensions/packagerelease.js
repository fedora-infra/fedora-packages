{  
  info: {
    consumes:['release_info'],
    author: 'John (J5) Palmieri <johnp@redhat.com>',
    version: '0.1',
    name: 'Release Info',
    summary: 'Display and manipulate releases',
    description: 'Displays the release information for a package and presents \
                  tools to manipulate that release.     \
                  \
                  Required Extension Point Data: \
                  \
                  - package_nvr: package full name including version and \
                                 release fields \
                  - build_id: the id of the build so we can get the tags \
                  '
    
  },
  
  run: function (data) {
    
    /************* Renders the release info into HTML ***************/                    
 
    render_updates = function(json)
      {
        console.log(json);
      };
    
    /************* Renders the releases into HTML ***************/                    
    render = function(json) 
      {
        var updates_match = /.*-(updates|testing|candidate)/;
        var query_updates = false;    

        var tag_div = jQuery("<div />");
        var tag_list = jQuery("<ul />");
        tag_div.append(tag_list);
        
        tags = json.tags;
        if (tags.length < 1) 
          {
            tag_list.append(jQuery("<li />").append("n/a"));
          }
        for (var i in tags) 
          {
            var name = tags[i]['name'];
            var list_item = jQuery("<li />").append(name);
            tag_list.append(list_item);
       
            if (name.match(updates_match)) 
              query_updates = true;  
          }
    
        if (query_updates)
          { 
            var burl = myfedora.get_page_base_url();
            params = {'package' : data.package_nvr,
                      'get_auth': true};
            jQuery.getJSON(burl + 'proxy/bodhi/get_info',
                           params,
                           render_updates);
          }
          
        var block = jQuery('#' + data.uid);
        block.html(tag_div);
      }
    
    /************* Converts tags to release name ***************/
    tags_to_release = function(json)
      {
        /* call render directly for now until we have this functionality*/
        render(json);
      }
      
    /* get the tags to process */
    var burl = myfedora.get_page_base_url();
    params = {'build_id' : data.build_id}
    jQuery.getJSON(burl + 'proxy/koji/get_tags',
                   params,
                   render);
    
    return myfedora.loading();
  }
}
