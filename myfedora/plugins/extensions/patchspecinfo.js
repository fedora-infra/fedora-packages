{  
  info: {
    consumes:['package_info'],
    author: 'John (J5) Palmieri <johnp@redhat.com>',
    version: '0.1',
    name: 'Package Spec and Patch Info',
    summary: 'Displays the latest spec and patches for the devel branch',
    description: 'Displays the spec file and patches for the development branch\
                  along with the link to the cvs repo \
                  \
                  Required Extension Point Data: \
                  \
                  - package: package name \
                  '
    
  },
  run: function (data) {
    var CVS_URL = 'http://cvs.fedoraproject.org/'
    var PROXY_CVS_URL = myfedora.get_page_base_url() + 'proxy/cvs/get_page';
    var PKGCVS_PATH = '/viewcvs/rpms/';
    
    /************* Renders the HTML ***************/                    
    render = function(html) 
      {
        var file_list = jQuery("<table/>");
        var spec_files = jQuery("a[name$='.spec']", html);
        var patch_files = jQuery("a[name$='.patch']", html);
        
        var expand_urls = function(element) {
          // get the revision link
          var p = element.parent();

          var n = p.next();
          var a = jQuery("a[href]", n);
          var revurl = a.attr("href");
          var el = element;
          var url = el.attr('src');
          
          if (url) {
             el.attr('src', CVS_URL + url);
          }
          
          url = el.attr('href');
          
          if (url) {
             el.attr('href', CVS_URL + revurl);
          }
          
          el = jQuery("img", element);
          
          url = el.attr('src');
          
          if (url) {
             el.attr('src', CVS_URL + url);
          }
          
        }
        
        var seperate_and_add_cells = function(element) {
          var coldiv = jQuery('<div />');
          var td = jQuery('<td />');
          var img = jQuery("img", element);
          
          var img_cpy = img.clone();
          img.replaceWith("");
          
          td.append(img_cpy);
          coldiv.append(td);

          td = jQuery('<td />');
          td.append(element);
          coldiv.append(td);

          return coldiv;
        } 
        
        var append_row_and_format = function(parent, elements) {
          for(i=0; i < elements.length; i++) {
            var row = jQuery("<tr/>");
            var a = jQuery(elements[i]);
            a.attr("target", "_blank");
            expand_urls(a);
            var cols = seperate_and_add_cells(a);
            row.append(cols);
            parent.append(row); 
          }
        }
       
        append_row_and_format(file_list, spec_files);
        append_row_and_format(file_list, patch_files);
        
        var block = jQuery('#' + data.uid + "_filelist");
        block.replaceWith(file_list);
      }
      
    /* get the html page to process */
    var proxyurl = PROXY_CVS_URL + PKGCVS_PATH + data.package + "/devel";
    var url = CVS_URL + PKGCVS_PATH + data.package
    
    jQuery.get(proxyurl,
               render,
               "html");
               
    var div = jQuery('<div class="panel"/>');
    var header=jQuery('<h3>Package Contents</h3>');
    div.append(header);
    var pkgcvs_link = jQuery("<a><strong>View the package source in Package CVS</strong></a>").attr("href", url);
    pkgcvs_link.attr("target", "_blank");
    div.append(pkgcvs_link);
    var devel_div = jQuery("<div><h4>Devel spec file and patches</h4></div>");
    var file_placeholder = jQuery("<table><tr><td>" + myfedora.loading() + "</td></tr></table>");
    file_placeholder.attr("id", data.uid + "_filelist");
    
    devel_div.append(file_placeholder);
    div.append(devel_div);
    div.addClass('list');
    
    return div;
  }
}
