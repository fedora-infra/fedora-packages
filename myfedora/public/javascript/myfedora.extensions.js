var _extensions = function(){};

_extensions.prototype = {
    _extension_cache: {},
    _extension_uid_counter: 0,
        
    grep_extensions: function()
      {
        var extension_points = $('script[type=text/x-myfedora-extpoint]');
        extension_points.each
          (
            function(i)
              {
                var ep = extension_points[i]
                var data = ep.text;
                data = myfedora.safe_json_parse(data);
                myfedora.extensions.load_extensions(data);
              }                 
          );
      },
    
    run_extensions: function (js, data)
      {
        
        //we trust the server so we can just eval the js
        // it should be a list of objects with a run method
        var obj_list = eval(js);
        
        console.log(obj_list);
        console.log(obj_list.length);
        for(var i = 0; i < obj_list.length; i++) {
          //clone our data and generate our uid so we are unique
          var d = new myfedora.shallow_clone(data);
          d.uid = "extension_" + this._extension_uid_counter + 
            "_" + (Math.floor(Math.random() * 10000000));
            
          //create a place to put this extension that they can call their own
          var div = jQuery("<div />").attr("id", d.uid);
          
          var append_div = jQuery("#" + data.placeholder_id);
          append_div.append(div);
          
          //run the script and parse in the results
          console.log(i);
          var result = obj_list[i].run(d);
          div.append(result);
          
          this._extension_uid_counter++;
        }
       
      },
    
    load_extensions: function (data) 
      {
        var ext_code = this._extension_cache[data.type];
        if (ext_code)
          {
            this.run_extensions(ext_code, data)
            return;
          }
        
        jQuery.get("/extensions?exttype=" + data.type, 
          function (js, err)
            {
              myfedora.extensions._extension_cache[data.type] = js;
              myfedora.extensions.run_extensions(js, data);
            } 
         );
      }
};

myfedora.extensions = new _extensions();

jQuery(document).ready(myfedora.extensions.grep_extensions)