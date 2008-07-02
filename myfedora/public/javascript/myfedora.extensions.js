var _extensions = function(){};

_extensions.prototype = {
    _extension_cache: {},
    _extension_deferred: {},
    _extension_uid_counter: 0,
        
    grep_extensions: function()
      {
        var extension_points = jQuery('script[type=text/x-myfedora-extpoint]');
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
        var obj_list = js;
        
        for(var i = 0; i < obj_list.length; i++) {
          //clone our data and generate our uid so we are unique
          var d = new myfedora.shallow_clone(data);
          d.uid = "extension_" + this._extension_uid_counter + 
            "_" + (Math.floor(Math.random() * 10000000));
            
          //create a place to put this extension that they can call their own
          var div = jQuery("<div />").attr("id", d.uid);
          div.hide();
          var append_div = jQuery("#" + data.placeholder_id);
          append_div.append(div);
          
          //run the script and parse in the results
          var result = obj_list[i].run(d);
          div.append(result);
          
          //show it
          if (data.effect) {
            eval("div." + data.effect);
          } else {
            div.show();
          }
          
          this._extension_uid_counter++;
        }
       
      },
    
    load_extensions: function (data) 
      {
        var ext_code = this._extension_cache[data.type];
        var ext_deferred = this._extension_deferred[data.type];
        if (ext_code)
          {
            this.run_extensions(ext_code, data);
            return; 
          }
        else if (ext_deferred)
          { 
            this._extension_deferred[data.type].push(data);
            return;
          }
        
        this._extension_deferred[data.type] = new Array();
        jQuery.get("/extensions?exttype=" + data.type, 
          function (js_string, err)
            {
              // we trust the server so we can just eval the js
              // it should be a list of objects with a run method
              var js = eval(js_string);
              
              // run this callback's extention
              myfedora.extensions.run_extensions(js, data);
              
              // now run the deferred extensions queued up while the scripts
              // were being downloaded
              var d = myfedora.extensions._extension_deferred[data.type].shift();
              while(d)
                {
                  myfedora.extensions.run_extensions(js, d);
                  d = myfedora.extensions._extension_deferred[data.type].shift();
                }
                
              myfedora.extensions._extension_cache[data.type] = js;
            } 
         );
      }
};

myfedora.extensions = new _extensions();

jQuery(document).ready(myfedora.extensions.grep_extensions)