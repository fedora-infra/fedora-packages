

/******** construct the menu base class ********/
var _menu_base = function(menu_id) {
  if (typeof(menu_id) == "string")
    {
      this.menu = jQuery("#" + menu_id);
    } 
  else
    {
      this.menu = menu_id;
    }
};

_menu_base.prototype = {
  menu: undefined,
  show_effect: undefined,
  hide_effect: undefined, 
  setup: function() {
    this.menu.addClass("menu");
  },
  
  hide: function() {
    this.menu.hide();
  },
  
  show: function() {
    this.menu.show();
  },
  
  fancy_hide: function() {
    var menu = this.menu;
    
    if (!this.hide_effect)
      {
        this.hide();
      }
    else
      {
        
        eval("menu." + this.hide_effect);
      }
  },
  
  fancy_show: function() {
    var menu = this.menu;
    
    if (!this.show_effect)
      {
        this.show();
      }
    else
      {
        eval("menu." + this.show_effect);
      }
  },
  
  set_show_effect: function(effect) {
    this.show_effect = effect;
  },
  
  set_hide_effect: function(effect) {
     this.hide_effect = effect;
  }
  
};

/******** construct the hover menu class ********/
var _hover_menu = function(menu_id) {
  var parent = new _menu_base(menu_id);
  myfedora.inherit(this, parent);
  this.setup();
  
  this.menu_parent = this.menu.parent();
 
  var self = this;
  this.menu_parent.hover(function() {
                           
                           self.fancy_show();
                           
                         },
                         function() {
                           
                           self.fancy_hide();
                    
                         });
};

_hover_menu.prototype = {
};

/******** construct the click menu class ********/


/******** construct the ellipsized text class ********/
var _ellipsized_text = function(blockid, morelink_text, lesslink_text, max_len) {
  this.div = jQuery('#' + blockid);
  this.morelink_text = morelink_text;
  this.lesslink_text = lesslink_text;
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
  },
  
  show: function() {
    var self = this;  
    this.div.hide();
    
    var s = jQuery('<span/>').text('[');
    var a = jQuery('<a/>').attr('href', '#').text(this.lesslink_text);
    a.click(function() {self.ellipsize(self); return false;});
    s.append(a);
    s.append(']');
    
    this.html = jQuery('<span/>').append(this.div.html());
    this.html.append(s);
    
    this.sanitize_tags();

    var el = this.calc_ellipse(this.div, this.max_len);
      
      
    s = jQuery('<span />').text(' [');
    a = jQuery('<a/>').attr('href', '#').text(this.morelink_text);
      
    this.lessdiv = el
      
    this.div.html(el);
      
      
    a.click(function() {self.unellipsize(self); return false;});
    s.append(a);
    s.append(']');
    el.append(s);
    
    this.div.show();
  },
  
  unellipsize: function(self) {
    self.div.hide();
    self.div.html(self.html);
    self.div.slideDown('fast');
  },
  
  ellipsize: function(self) {

    self.div.html(self.lessdiv);
    self.div.show();
  },
};


/******** construct the UI module ********/
var _ui = function(){};

_ui = {
  menu_base: _menu_base, 
  hover_menu: _hover_menu,
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

