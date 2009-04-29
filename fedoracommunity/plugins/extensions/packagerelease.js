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
                  - builder: the person who built the package \
                  - identity: the identity of the person who is logged in \
                  '
    
  },
  
  run: function (data) {
    
    /************* Renders the release info into HTML ***************/                    
 
    var render_updates = function(json)
      {
        var add_stable_action = false;
        var add_testing_action = false;
        var add_cancel_action = false;
        
        if (json.num_items == 0 && data.identity == data.builder)
          {
            add_stable_action = true;
            add_testing_action = true;
          } else if (json.num_items > 0) {
            var up = json.updates[0];
            if (!up.can_modify)
              return;
            
            if (up.status == 'stable')
              return;
              
            if (up.request)
              {
                add_cancel_action = true;
              }
            else if (up.status == 'testing')
              {
                add_stable_action = true;
              } 
            else
              {
                add_stable_action == true;
                add_testing_action == true;
              }              
          }
        else
          {
            return;
          }
          
        var block = jQuery('#' + data.uid);
        block.append('[ ');
        if (add_stable_action)
          {
            block.append('push to stable');
            if (add_testing_action)
              block.append(' | ');
          }
          
        if (add_testing_action)
          {
            block.append('push to testing');
          }
          
        if (add_cancel_action)
          {
            block.append('cancel push');
          }
        
        block.append(' ]');
      };
    
    var updates_match = /.*-(updates|testing|candidate)/;
    /************* Renders the releases into HTML ***************/                    
    render = function(json) 
      {
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
       
            if (updates_match.test(name)) 
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
        
      }
      
    /* get the tags to process */
    var burl = myfedora.get_page_base_url();
    params = {'build_id' : data.build_id};
    jQuery.getJSON(burl + 'proxy/koji/get_tags',
                   params,
                   render);
    
    return myfedora.loading();
  }
}
