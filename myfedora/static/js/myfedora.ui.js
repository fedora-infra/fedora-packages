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
