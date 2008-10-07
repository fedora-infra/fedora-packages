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
    var burl = myfedora.get_page_base_url();
    var PROXY_URL = burl + 'proxy/fas/get_todo_list_page';
    var FAS_URL = 'http://admin.fedoraproject.org/accounts/';
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
            console.log(i);
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
 