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
            console.log(e);
            return false;
          }
       },
       
     shallow_clone: function (obj) 
       {
         for (i in obj) 
           {
             this[i] = obj[i];
           }
       }
     
};