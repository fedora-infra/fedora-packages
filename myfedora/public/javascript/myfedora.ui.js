

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


/******** construct the UI module ********/
var _ui = function(){};

_ui = {
  menu_base: _menu_base, 
  hover_menu: _hover_menu 
};

myfedora.ui = _ui;

