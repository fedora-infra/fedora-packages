

var _mf_current_hover_menu = "";

function mf_menu_hover_start(menu_name)
{
    var div;

    if (_mf_current_hover_menu)
      return;

    _mf_current_hover_menu = "#" + menu_name;
    div = $(_mf_current_hover_menu);

    div.fadeIn('fast');   
}

function _mf_menu_hover_fadeout(menu_name)
{
    if (_mf_current_hover_menu != menu_name)
      $(menu_name).fadeOut('fast');
}

function mf_menu_hover_stop()
{
    setTimeout("_mf_menu_hover_fadeout('" + _mf_current_hover_menu + "')", 50);
    _mf_current_hover_menu = "";
}

function mf_replace_block_async(block_name, url, params, user_callback, user_data)
{
    function _mf_json_callback(data) 
          {
            var block = $("#" + block_name);
            var html = user_callback(block, data, user_data);
            if (html != undefined)
              block.html(html);
          } 

    if (params == undefined)
      params = {};

    if (params.callback == '?') {
      delete(params.callback);
      url += '?callback=?';
    }
    
    params.tg_format = 'json';

    $.getJSON(url, params, _mf_json_callback); 
}

function mf_show_overlay(id, content_div, z) 
{
  var ww = $(window).width();
  var wh = $(window).height();
  var dh = $(document).height();

  var master_div = $('#' + id);
  var overlay_div = $("<div />");

  master_div.css({'z-index': z});
  overlay_div.css(
           { position: 'absolute', 
             opacity: .7,
             height: dh,
             width: ww,
             top: 0,
             left: 0,
             'background-color': '#555555',
             'z-index': z
           });

  content_div.css(
           { position: 'absolute',
             height: wh - 160,
             width: ww - 160,
             top: 80,
             left: 80,
             overflow: 'auto',
             'z-index': z
           });
             

  master_div.html(overlay_div);
  master_div.append(content_div);
  master_div.fadeTo("slow", 1);

  return master_div;
}

function mf_hide_overlay(id)
{
  var overlay_div = $('#' + id);

  overlay_div.css(
           {
             opacity: 0,
             'z-index': -1
           });
 overlay_div.html("");
}
