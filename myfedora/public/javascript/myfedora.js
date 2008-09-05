var _myfedora = window.myfedora;

// Create an empty object we will then extend
var myfedora = window.myfedora = function () {};

myfedora = {
    parse_query_string: function (url)
      {
        var result = {};

        var queryString = undefined;
        var urlComponents = url.split(/\?/);
        if (urlComponents.length == 2)
          {
            queryString = urlComponents[1];
          }
        else
          {
            return undefined;
          }
          
        if (queryString.charAt(0) == '?') queryString = queryString.substring(1);

        // replace plus signs in the query string with spaces
        queryString = queryString.replace('+', ' ');

        // split the query string around ampersands and semicolons
        var queryComponents = queryString.split(/[&;]/g);

        for (var i = 0; i < queryComponents.length; i++)
          {
          
            var keyValuePair = queryComponents[i].split('=');
            var key = decodeURIComponent(keyValuePair[0]);
            var value = decodeURIComponent(keyValuePair[1]);

            if (!result[key]) 
              result[key] = [];
              
            result[key].push((keyValuePair.length == 1) ? '' : value);
          
          }

        return result;
      },
    
    safe_json_parse: function(s) 
      {
        try 
          {
            if (/[^,:{}\[\]0-9.\-+Eaeflnr-u \n\r\t]/.test(s.replace(/"(\\.|[^"\\])*"/g, '')))
              {
                return eval('(' + s + ')');
              }
          }
        catch (e) 
          {
            console.log("Error parsing json in safe_json_parse - ");
            console.log(e);
            return false;
          }
       },
     
     loading: function()
       {
         /* TODO: return an animated spinner */
         return 'Loading...'
       },
       
     shallow_clone: function(obj) 
       {
         var i;
         for (i in obj) 
           {
             this[i] = obj[i];
           }
       },
       
     inherit: function(self, parent)
       { 
         var i;
         for (i in parent) 
           {
              if (i != "prototype")
               {
                 self[i] = parent[i];
               }
           }
       },
       
     guess_client_arch: function(arch_default)
       {
         arch = arch_default;

         re = /Linux ([\d\w]+);/;
         match = re.exec(navigator.userAgent);
        
         a = match[1];
         if (a) 
           {
             arch = a;
           }
          
         // return a list of possible matches for i386 and x86_64
         x86_arches = ['x86_64', 'i686', 'i586', 'i486', 'i386', 'noarch'];
         if (arch == 'i686') {
           arch = x86_arches.slice(1);
         } else if (arch == 'i586') {
           arch = x86_arches.slice(2);
         } else if (arch == 'i486') {
           arch = x86_arches.slice(3);
         } else if (arch == 'x86_64') {
           arch = x86_arches;
         } else {
           arch = [arch];
         }

         return arch;
       }
};