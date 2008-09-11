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
    var PROXY_CVS_URL = myfedora.get_page_base_url() + '/proxy/cvs/get_page';
    var PKGCVS_PATH = '/viewcvs/rpms/';
    
    /************* Renders the HTML ***************/                    
    render = function(html) 
      {
        var file_ul = jQuery("<ul/>");
        var spec_files = jQuery("a[name$='.spec']", html);
        var patch_files = jQuery("a[name$='.patch']", html);
        
        var expand_urls = function(element) {
          // get the revision link
          var p = element.parent();

          var n = p.next();
          var a = jQuery("a[href]", n);
          var revurl = a.attr("href");
          var el = element;
          url = el.attr('src');
          
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
        
        var append_li_and_format = function(parent, elements) {
          for(i=0; i < elements.length; i++) {
            var li = jQuery("<li/>");
            var a = jQuery(elements[i]);
            a.attr("target", "_blank");
            expand_urls(a);
            li.append(a);
            parent.append(li); 
          }
        }
       
        append_li_and_format(file_ul, spec_files);
        append_li_and_format(file_ul, patch_files);
        
        var block = jQuery('#' + data.uid + "_filelist");
        block.replaceWith(file_ul);
      }
      
    /* get the html page to process */
    var proxyurl = PROXY_CVS_URL + PKGCVS_PATH + data.package + "/devel";
    var url = CVS_URL + PKGCVS_PATH + data.package
  
    jQuery.get(proxyurl,
               render,
               "html");
 
    var div = jQuery("<div />");
    var pkgcvs_link = jQuery("<a><strong>View the package source in Package CVS</strong></a>").attr("href", url);
    pkgcvs_link.attr("target", "_blank");
    div.append(pkgcvs_link);
    var devel_div = jQuery("<div><strong>Devel spec file and patches:</strong></div>");
    var file_ul = jQuery("<ul />").attr("id", data.uid + "_filelist");
    file_ul.append(jQuery("<li>" + myfedora.loading() + "</li>"));
    devel_div.append(file_ul);
    div.append(devel_div);
    
    return div;
  }
}
