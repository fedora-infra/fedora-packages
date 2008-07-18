var _myfedora = window.myfedora;

// Create an empty object we will then extend
var myfedora = window.myfedora = function () {};

myfedora = {
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