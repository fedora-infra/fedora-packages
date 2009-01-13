

/******** base widget class ********/
var _base_widget = function(block_id) {
  if (typeof(block_id) == "string")
    {
      this.block = jQuery("#" + block_id);
    } 
  else
    {
      this.block = block_id;
    }
};

_base_widget.prototype = {
  block: undefined,
  show_effect: undefined,
  hide_effect: undefined, 
  setup: function() {
    this.hide();
  },
  
  hide: function() {
    var block = this.block;
    
    if (!this.hide_effect)
      {
        this.block.hide();
      }
    else
      {    
        eval("block." + this.hide_effect);
      }
  },
  
  show: function() {
    var block = this.block;
    
    if (!this.show_effect)
      {
        this.block.show();
      }
    else
      {
        eval("block." + this.show_effect);
      }
  },
  
  set_show_effect: function(effect) {
    this.show_effect = effect;
  },
  
  set_hide_effect: function(effect) {
     this.hide_effect = effect;
  }
  
};

/******** hover menu class ********/
var _hover_menu = function(menu_id) {
  var parent = new _base_widget(menu_id);
  myfedora.inherit(this, parent);
  this.setup();
  
  this.menu_parent = this.block.parent();
 
  var self = this;
  this.menu_parent.hover(function() {
                           
                           self.show();
                           
                         },
                         function() {
                           
                           self.hide();
                    
                         });
};

_hover_menu.prototype = {
};

/******** click menu class ********/

/******** autocomplete entry class **********/
var _autocomplete_entry = function(entry_id, min_chars, js_search_callback) {
  this.entry_box = jQuery("#" + entry_id);
  var menu = jQuery("<div />").css({"z-index": 100,
                                    "background-color": "white",
                                    "position": "absolute",
                                    "overflow": "auto",
                                    "max-height": "200px",
                                    "border": "1px"
                                    });
                                         
  this.entry_box.parent().append(menu);
  this.entry_box.attr("autocomplete", "off");                               
                                       
  var parent = new _base_widget(menu);
  myfedora.inherit(this, parent);
  this.setup();
  
  this.min_chars = min_chars
  this.menu = menu
  var current_highlight = undefined;
  var self = this;
  var change_cb = function(e) 
    {
      switch (e.keyCode)
        {
          case 14:
          case 40:
          case 38:
            return false;
        }
        
      current_highlight = undefined;
      self.menu.css("left", self.entry_box[0].offsetLeft + "px");
      self.menu.css("top", self.entry_box[0].offsetTop + self.entry_box[0].height + "px");
      var entry = e.currentTarget
      var got_values = function(list) 
        {
          var s = entry.value;
          if (list && s)
            {
              var modified = false;
              var html_list = jQuery("<ul />").attr("id", entry_id + "_list");
              for (i in list) 
                {
                  var key = list[i][1]
                  if (key.indexOf(s) == 0)
                    { 
                      modified = true;
                      var label = list[i][0]
                      var li = jQuery("<li />");
                      li.append("<div>" + label + "</div><div class='key'>" + key + "</div><hr />");
                  
                      html_list.append(li);
                    }
                }
                
              if (modified)
                {
                  self.block.html(html_list);
                  self.show();
                }
              else
                {
                  self.hide();
                }
            }
          else
            {
              self.hide();
            }
        }
      
      if (js_search_callback && (entry.value.length) >= self.min_chars)
        {
          js_search_callback(entry.value, got_values);
        }
      else
        {
          self.hide();
        }
    }
  
  var keypress_cb = function(e)
    {
      var ul = jQuery("#" + entry_id + "_list");
      var c = jQuery("li", ul);
      var matched = false;
      switch(e.keyCode)
        {
          case 40: // down
            matched = true;
            if (current_highlight != undefined)
              current_highlight++;
            else
              current_highlight = 0;
            break;
          case 38: // up
            matched = true;
            if (current_highlight != undefined)
              current_highlight--;
            else
              current_highlight = -1;
            break;
          case 13: // enter
            matched = true;
            self.entry_box.form.submit();
            break;
        }
        
        if (current_highlight == undefined)
          return !matched;
          
        if (current_highlight < 0)
          current_highlight = c.length - 1;
        else if (current_highlight >= c.length)
          current_highlight = 0;
        
        c.css("background-color", "white");  
        var h = jQuery(c[current_highlight]);
        h.css("background-color", "blue");
        self.entry_box[0].value = jQuery(".key", h).text();
        
        return !matched;
    }
  
  self.entry_box.keyup(change_cb);
  self.entry_box.keypress(keypress_cb);
}
  

/******** lightbox class **********/

var _lightbox = function(block_id, zindex) {
  var parent = new _base_widget(block_id);
  myfedora.inherit(this, parent);
  this.setup();
  
  var main_box = jQuery("<div />").addClass("lightbox-parent");;
  var dark_box = jQuery("<div />").addClass("lightbox-black");
  dark_box.show();
  
  var content = this.block;
  content.show();
  content.parent().append(main_box);
  
  var light_box = jQuery("<div />").addClass("lightbox-white");
  light_box.show();
  
  var self = this;
  var hide = function (){
    self.hide(); 
    return false;
  }
  
  var close_link = jQuery("<a href='#'/>").text("[X]Close").click(hide);           
  light_box.append(close_link);
  light_box.append(content);
  light_box.append(close_link.clone(true));
  main_box.append(dark_box);
  main_box.append(light_box);
  
  this.block = main_box;
  this.block.hide();
};

_lightbox.prototype = {
};

/******** ellipsized text class ********/
var _ellipsized_text = function(blockid, max_len, show_more_object, show_more_text) {
  
  this.show_more_object = undefined;
  if (show_more_object) {
    this.show_more_object = show_more_object;
    
    if (!show_more_text) {
      show_more_text = 'more...'
    }
  }
  
  this.div = jQuery('#' + blockid);
  this.show_more_text = show_more_text;
 
  this.max_len = max_len;

};

_ellipsized_text.prototype =  {
  calc_ellipse: function(html, size) {
    var text = this.div.text();
    
    if (text.length > this.max_len)
        text = text.substr(0, this.max_len) + '...';
        
    var result = jQuery('<span />');
    result.append(text);
    
    return result
  },
  
  sanitize_tags: function() {
    // add a blank target to links
    var a = jQuery('a', this.div);
    
    a.attr('target', '_blank');
    
    if (this.lightbox_div) {
      a = jQuery('a', this.lightbox_div);
      a.attr('target', '_blank');
    }
  },
  
  show: function() {
    var self = this;  
    this.div.hide();
    
    this.sanitize_tags();

    var el = this.calc_ellipse(this.div, this.max_len);
      
    this.lessdiv = el
      
    this.div.html(el);
      
    if (this.show_more_object) {
      s = jQuery('<span />').text(' [');
      a = jQuery('<a/>').attr('href', '#').text(this.show_more_text);
      a.click(function() {self.show_more_object .show(); return false;});
      s.append(a);
      s.append(']');
      el.append(s);
    }
    
    this.div.show();
  },
};


/******** construct the UI module ********/
var _ui = function(){};

_ui = {
  base_widget: _base_widget, 
  hover_menu: _hover_menu,
  autocomplete_entry: _autocomplete_entry,
  lightbox: _lightbox,
  ellipsized_text: _ellipsized_text,
  
  generate_widget_param_url: function(id, req_params) {
    var query_string = document.location.search;
    var path = document.location.pathname;
    var elements = myfedora.parse_query_string(query_string);
    
    if (! elements) {
      elements = {};
    }
    
    for (var k in req_params) {
      var kid = id + "_" + k;
      elements[kid] = req_params[k];
    }
    
    query_string = "?";
    var add_amp = false;
    for (var k in elements) {
      if (add_amp) { 
        k += "&"; 
      } else {
        add_amp = true;
      }
      
      query_string += k + "=" + elements[k];
    }
    
    return path + query_string;
  },
  
  go_to: function(id, req_params) {
    document.location.href = myfedora.ui.generate_widget_param_url(id, req_params);
  }
};

myfedora.ui = _ui;

//# Quit using myfedora.ui and simply use jQuery.extend
//############### make a moksha datagrid ######################
(function($) {
  $.widget("ui.mokshagrid",{
    /* public method list */
    public_signals: ["ready", "refresh_data"],
    bind_api: function(api_list) {
        var self = this;
        for (var i in api_list) {
            var pm = api_list[i];
            var name = pm + ".mokshagrid";
            
            // proxy pattern (used for javascripts busted scoping rules)
            (function() {
                var proxied = self[pm];
                if (!proxied)
                    throw ('ERROR: binding api "' + pm + '" failed - method does not exist.'); 
            
                self.element.unbind(name).bind(name,
                    function() {
                        var args = []
                        for (var ai=1; ai < arguments.length; ai++) {
                            args.push(arguments[ai]);
                        }
                        
                        return proxied.apply(self, args);
                    });
            })();
        }
    },
    
    bind_public_api: function() {
        this.bind_api(this.public_methods);
        this.bind_api(this.public_signals);
    },
    
    /* methods */
    
    init: function() {
      var self = this;
      var o = self.options;
    
      self.$visible_rows = [];

      self.bind_public_api();

      // add placeholder for row appends
      self.$rowplaceholder = jQuery('<span />').addClass('moksha_rowplaceholder');
      self.$rowplaceholder.hide();
      var rowtemplate = jQuery('.rowtemplate',self.element);
      rowtemplate.after(self.$rowplaceholder);
      
      // hack to get the full html of the template including the root tag
      // this also removes the template from the document
      var container_div = jQuery('<div />');
      var html = container_div.append(rowtemplate).html();
      
      self.$template = jQuery.template(html, {regx:'moksha'}).compile();
      
      self.$headers =  $('th:has(a[href])', this.element);
      //self.$headers = this.$ths.map(function() { return $('a', this)[0]; });
      self.$headers.unbind(o.event + '.mokshagrid').bind(o.event + '.mokshagrid', function(event) {
        var ckey = o.sort_key;
        var corder = o.sort_order;
        console.log(event)
        var key = event.originalTarget.hash.substr(1);
      
        if (key == ckey) {
            if (corder == 'decending') {
                corder = 'acending';
            } else {
                corder = 'decending';
            }
        } else {
            corder = 'decending';
        }
        
        self.options['sort_key'] = key;
        self.options['sort_order'] = corder;
            
        self.request_data_refresh();

        return false;
      })
          
      jQuery(document).bind('ready', function (event) {
                                 self.element.trigger('ready', event);
                             });
    },
    
    destroy: function() {
        this.$headers.unbind('.mokshagrid');
        this.element.unbind('.mokshagrid');
    },
    
    clear: function() {
       var self = this;
       var rows = self.$visible_rows;
       for (i in rows)
           rows[i].replaceWith('');
       
       self.$visible_rows = [];
    },
    
    insert_row: function(i, row_data) {
        var self = this;
        var o = self.options
        var rows = self.$visible_rows;
        var row_count = self.visible_row_count();
      
        // store the widget for this element
        jQuery.data(self.element, 'mokshagrid', self);
        
        // do nothing if we are asked to insert passed
        // the number of rows being displayed
        if (i >= o.rows_per_page || (i == -1  && row_count >= o.rows_per_page))
            return;
            
        var new_row = jQuery(self.$template.apply(row_data));
        
        if (i == -1 || row_count == i) {
            // append to the end of the tracking array and the table dom
            rows.push(new_row);
            self.$rowplaceholder.before(new_row);
        } else {
            
            // insert before i element in the tracking array and table dom
            rows[i].before(new_row);
            rows.splice(i, 0, new_row);
            
            // if there is one too many rows remove the last one
            if (row_count == o.rows_per_page)
                self.remove_row(o.rows_per_page);
        }
        
        new_row.show();
    },
    
    append_row: function(row_data) {
        var self = this;
        self.insert_row(-1, row_data);
    },
    
    remove_row: function(i) {
        var self = this;
        var rows = self.$visible_rows;
        rows[i].replaceWith('');
        rows.splice(i,1);
    },
    
    connector_query: function(connector, path, dispatch_data, callback) {
        //TODO: implement a json loading method 
        //      which starts and stops a loading
        //      throbber
        
        if (dispatch_data)
            path = '/moksha_connector/' + connector + '/query/' + path + '/' + $.toJSON(dispatch_data);
            
        console.log(path);
        var xmlrequest = jQuery.getJSON(path, {}, callback);
    },
    
    request_data_refresh: function(event) {
        // TODO: allow an optional rows_requested parameter
        var self = this
        
        var o = self.options;
        
        // figure out which row to start with
        var rpp = o.rows_per_page;
        var start_row = (o.page_num - 1) * rpp;
          
        // setup the search criteria
        var search_criteria = {
            filters: o.filters,
            start_row: start_row,
            rows_requested: rpp,
            sort_key: o.sort_key,
            sort_order: o.sort_order,
        }
        
        console.log(search_criteria);
        // TODO: Only trigger refresh signal if we have a cache miss
        self.element.trigger('refresh_data', [event, search_criteria]);
    },
    
    /* Signals */
    ready: function(event, user_data) {
        self = this;
        self.request_data_refresh();
    },
    
    refresh_data: function(event, search_criteria) {},
    
    /* Getter/Setters */
    
    visible_row_count: function() {
        var self = this;
        return self.$visible_rows.length;
    },
  })
  
  $.extend($.ui.mokshagrid, {
          version: '@VERSION',
          getters: 'visible_row_count',
          defaults: {
                 event: 'click',
                 rows_per_page: 10,
                 page_num: 1,
                 total_rows: 0,
                 filters: {},
                 unique_key: undefined,
                 sort_key: undefined,
                 sort_order: "decending",
                 loading_throbber: ["Loading",    // list of img urls or text
                                    "Loading.", 
                                    "Loading..",  
                                    "Loading..."]  
          }
  });
  
$.extend( $.template.regx , {
             moksha:/\@\{([\w-]+)(?:\:([\w\.]*)(?:\((.*?)?\))?)?\}/g
           }
);
  
  
})(jQuery);
  